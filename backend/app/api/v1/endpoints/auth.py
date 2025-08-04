from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_current_active_user
)
from app.core.password import (
    verify_password,
    get_password_hash
)
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserOAuth,
    UserResponse,
    PasswordChange,
    PasswordReset,
    PasswordResetConfirm,
    TelegramConnect
)
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.email_service import EmailService

logger = structlog.get_logger()
router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Регистрация нового пользователя
    """
    user_service = UserService(db)
    auth_service = AuthService(db)
    
    # Проверка существования пользователя
    if await user_service.get_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    if await user_service.get_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )
    
    # Создание пользователя
    user = await auth_service.create_user(user_data)
    
    # Отправка приветственного email
    email_service = EmailService()
    await email_service.send_welcome_email(user.email, user.username)
    
    logger.info("New user registered", user_id=user.id, email=user.email)
    
    return user


@router.post("/login")
async def login(
    user_data: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Вход в систему
    """
    auth_service = AuthService(db)
    
    # Аутентификация пользователя
    user = await auth_service.authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is not active"
        )
    
    # Создание токенов
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
    # Установка httpOnly куки
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    
    # Обновление времени последнего входа
    await auth_service.update_last_login(user.id)
    
    logger.info("User logged in", user_id=user.id, email=user.email)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/oauth/{provider}")
async def oauth_login(
    provider: str,
    oauth_data: UserOAuth,
    response: Response,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    OAuth аутентификация (Google, Telegram)
    """
    auth_service = AuthService(db)
    
    if provider not in ["google", "telegram"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported OAuth provider"
        )
    
    # Обработка OAuth
    user = await auth_service.oauth_authenticate(provider, oauth_data)
    
    # Создание токенов
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
    # Установка куки
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    
    logger.info("User logged in via OAuth", user_id=user.id, provider=provider)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/refresh")
async def refresh_token(
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
) -> Any:
    """
    Обновление access token
    """
    # Создание нового access token
    access_token = create_access_token(
        data={"sub": str(current_user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Обновление куки
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(response: Response) -> Any:
    """
    Выход из системы
    """
    # Удаление куки
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserResponse = Depends(get_current_active_user)
) -> Any:
    """
    Получение информации о текущем пользователе
    """
    return current_user


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: UserResponse = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Изменение пароля
    """
    auth_service = AuthService(db)
    
    # Проверка текущего пароля
    if not await auth_service.verify_password(current_user.id, password_data.current_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Изменение пароля
    await auth_service.change_password(current_user.id, password_data.new_password)
    
    logger.info("User changed password", user_id=current_user.id)
    
    return {"message": "Password changed successfully"}


@router.post("/password-reset")
async def password_reset(
    reset_data: PasswordReset,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Запрос сброса пароля
    """
    auth_service = AuthService(db)
    email_service = EmailService()
    
    # Создание токена для сброса пароля
    token = await auth_service.create_password_reset_token(reset_data.email)
    
    if token:
        # Отправка email с токеном
        await email_service.send_password_reset_email(reset_data.email, token)
        
        logger.info("Password reset requested", email=reset_data.email)
    
    # Всегда возвращаем успех для безопасности
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/password-reset/confirm")
async def password_reset_confirm(
    reset_data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Подтверждение сброса пароля
    """
    auth_service = AuthService(db)
    
    # Подтверждение токена и изменение пароля
    success = await auth_service.confirm_password_reset(
        reset_data.token,
        reset_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    logger.info("Password reset confirmed", token=reset_data.token)
    
    return {"message": "Password reset successfully"}


@router.post("/telegram/connect")
async def connect_telegram(
    telegram_data: TelegramConnect,
    current_user: UserResponse = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Подключение Telegram аккаунта
    """
    auth_service = AuthService(db)
    
    # Подключение Telegram
    success = await auth_service.connect_telegram(
        current_user.id,
        telegram_data
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to connect Telegram account"
        )
    
    logger.info("Telegram connected", user_id=current_user.id, telegram_id=telegram_data.telegram_id)
    
    return {"message": "Telegram account connected successfully"}


@router.post("/telegram/disconnect")
async def disconnect_telegram(
    current_user: UserResponse = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Отключение Telegram аккаунта
    """
    auth_service = AuthService(db)
    
    # Отключение Telegram
    await auth_service.disconnect_telegram(current_user.id)
    
    logger.info("Telegram disconnected", user_id=current_user.id)
    
    return {"message": "Telegram account disconnected successfully"} 