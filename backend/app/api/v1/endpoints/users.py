from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_admin_user
from app.schemas.user import (
    UserResponse, UserUpdate, UserProfile, UserList, 
    PasswordChange, TelegramConnect, UserPreferences
)
from app.services.user_service import UserService
from app.models.user import User

logger = structlog.get_logger()
router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Получение информации о текущем пользователе"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Обновление профиля текущего пользователя"""
    user_service = UserService(db)
    
    # Проверка уникальности username если он изменяется
    if user_data.username and user_data.username != current_user.username:
        existing_user = await user_service.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    updated_user = await user_service.update_user(str(current_user.id), user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user


@router.get("/me/profile", response_model=UserProfile)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Получение расширенного профиля текущего пользователя"""
    user_service = UserService(db)
    
    profile_data = await user_service.get_user_profile(str(current_user.id))
    if not profile_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    return profile_data


@router.post("/me/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Изменение пароля текущего пользователя"""
    user_service = UserService(db)
    
    # Проверка текущего пароля
    if not await user_service.verify_user_password(str(current_user.id), password_data.current_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Изменение пароля
    success = await user_service.change_password(str(current_user.id), password_data.new_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )
    
    return {"message": "Password changed successfully"}


@router.post("/me/telegram/connect")
async def connect_telegram(
    telegram_data: TelegramConnect,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Подключение Telegram аккаунта"""
    user_service = UserService(db)
    
    # Проверка, что Telegram ID не занят
    existing_user = await user_service.get_by_telegram_id(telegram_data.telegram_id)
    if existing_user and str(existing_user.id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Telegram account already connected to another user"
        )
    
    # Обновление данных пользователя
    update_data = {
        "telegram_id": telegram_data.telegram_id,
        "telegram_username": telegram_data.telegram_username,
        "telegram_notifications": True
    }
    
    if telegram_data.first_name:
        update_data["first_name"] = telegram_data.first_name
    if telegram_data.last_name:
        update_data["last_name"] = telegram_data.last_name
    
    updated_user = await user_service.update_user(str(current_user.id), update_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect Telegram account"
        )
    
    return {"message": "Telegram account connected successfully"}


@router.post("/me/telegram/disconnect")
async def disconnect_telegram(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Отключение Telegram аккаунта"""
    user_service = UserService(db)
    
    update_data = {
        "telegram_id": None,
        "telegram_username": None,
        "telegram_notifications": False
    }
    
    updated_user = await user_service.update_user(str(current_user.id), update_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to disconnect Telegram account"
        )
    
    return {"message": "Telegram account disconnected successfully"}


@router.get("/{username}", response_model=UserProfile)
async def get_user_profile(
    username: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Получение профиля пользователя по username"""
    user_service = UserService(db)
    
    # Получение пользователя по username
    user = await user_service.get_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Проверка приватности профиля
    if not user.is_public_profile and str(user.id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Profile is private"
        )
    
    profile_data = await user_service.get_user_profile(str(user.id))
    if not profile_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    return profile_data


@router.post("/{username}/follow")
async def follow_user(
    username: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Подписка на пользователя"""
    user_service = UserService(db)
    
    # Получение пользователя для подписки
    user_to_follow = await user_service.get_by_username(username)
    if not user_to_follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Проверка, что не подписываемся на себя
    if str(user_to_follow.id) == str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot follow yourself"
        )
    
    success = await user_service.follow_user(str(current_user.id), str(user_to_follow.id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to follow user"
        )
    
    return {"message": f"Successfully followed {username}"}


@router.delete("/{username}/follow")
async def unfollow_user(
    username: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Отписка от пользователя"""
    user_service = UserService(db)
    
    # Получение пользователя для отписки
    user_to_unfollow = await user_service.get_by_username(username)
    if not user_to_unfollow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    success = await user_service.unfollow_user(str(current_user.id), str(user_to_unfollow.id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not following this user"
        )
    
    return {"message": f"Successfully unfollowed {username}"}


@router.get("/{username}/followers")
async def get_user_followers(
    username: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Получение списка подписчиков пользователя"""
    user_service = UserService(db)
    
    # Получение пользователя
    user = await user_service.get_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Проверка приватности профиля
    if not user.is_public_profile and str(user.id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Profile is private"
        )
    
    followers = await user_service.get_followers(str(user.id), skip, limit)
    return {"followers": followers, "total": len(followers)}


@router.get("/{username}/following")
async def get_user_following(
    username: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Получение списка подписок пользователя"""
    user_service = UserService(db)
    
    # Получение пользователя
    user = await user_service.get_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Проверка приватности профиля
    if not user.is_public_profile and str(user.id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Profile is private"
        )
    
    following = await user_service.get_following(str(user.id), skip, limit)
    return {"following": following, "total": len(following)}


# Административные эндпоинты
@router.get("/", response_model=UserList)
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: str = Query(None),
    role: str = Query(None),
    status: str = Query(None),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Получение списка пользователей (только для администраторов)"""
    user_service = UserService(db)
    
    users = await user_service.get_users(skip, limit, search, role, status)
    total = len(users)  # В реальном приложении нужно отдельно считать общее количество
    
    return {
        "users": users,
        "total": total,
        "page": skip // limit + 1,
        "per_page": limit,
        "has_next": len(users) == limit,
        "has_prev": skip > 0
    } 