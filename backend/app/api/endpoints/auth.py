"""
Аутентификация endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.core.database import get_db
from app.core.security import security_utils, security
from app.models.user import User, UserRole
from app.schemas.auth import (
    UserCreate, UserLogin, TokenResponse, 
    PasswordReset, PasswordResetConfirm
)
from app.services.user_service import UserService
from app.services.email_service import EmailService

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# Схемы для запросов
class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict

@router.post("/register", response_model=AuthResponse)
@limiter.limit("5/minute")
async def register(
    request: Request,
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Регистрация нового пользователя"""
    user_service = UserService(db)
    
    # Проверка существования пользователя
    existing_user = await user_service.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    existing_username = await user_service.get_by_username(user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken"
        )
    
    # Создание пользователя
    user = await user_service.create_user(user_data)
    
    # Генерация токенов
    access_token = security_utils.create_access_token(subject=user.id)
    refresh_token = security_utils.create_refresh_token(subject=user.id)
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user.public_profile
    )

@router.post("/login", response_model=AuthResponse)
@limiter.limit("10/minute")
async def login(
    request: Request,
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Вход в систему"""
    user_service = UserService(db)
    
    # Поиск пользователя
    user = await user_service.get_by_email(login_data.email)
    if not user or not security_utils.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is disabled"
        )
    
    # Обновление времени последнего входа
    await user_service.update_last_login(user.id)
    
    # Генерация токенов
    access_token = security_utils.create_access_token(subject=user.id)
    refresh_token = security_utils.create_refresh_token(subject=user.id)
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user.public_profile
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Обновление access токена"""
    token = credentials.credentials
    user_id = security_utils.verify_token(token, token_type="refresh")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_service = UserService(db)
    user = await user_service.get_by_id(int(user_id))
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Генерация нового access токена
    access_token = security_utils.create_access_token(subject=user.id)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )

@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Выход из системы"""
    # В продакшене здесь можно добавить токен в blacklist
    return {"message": "Successfully logged out"}

@router.post("/password-reset")
@limiter.limit("3/minute")
async def request_password_reset(
    request: Request,
    reset_data: PasswordReset,
    db: AsyncSession = Depends(get_db)
):
    """Запрос сброса пароля"""
    user_service = UserService(db)
    user = await user_service.get_by_email(reset_data.email)
    
    if user:
        # Генерация токена сброса
        reset_token = security_utils.generate_password_reset_token(user.email)
        
        # Отправка email (через Celery)
        email_service = EmailService()
        await email_service.send_password_reset_email(user.email, reset_token)
    
    # Всегда возвращаем success для безопасности
    return {"message": "If the email exists, password reset instructions have been sent"}

@router.post("/password-reset/confirm")
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
):
    """Подтверждение сброса пароля"""
    email = security_utils.verify_password_reset_token(reset_data.token)
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    user_service = UserService(db)
    user = await user_service.get_by_email(email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Обновление пароля
    await user_service.update_password(user.id, reset_data.new_password)
    
    return {"message": "Password has been reset successfully"}

@router.get("/me")
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Получение информации о текущем пользователе"""
    token = credentials.credentials
    user_id = security_utils.verify_token(token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user_service = UserService(db)
    user = await user_service.get_by_id(int(user_id))
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user.public_profile
