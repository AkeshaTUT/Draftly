from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timedelta
import uuid
import structlog

from app.models.user import User, UserRole, UserStatus
from app.schemas.user import UserCreate, UserOAuth, TelegramConnect
from app.core.password import get_password_hash, verify_password
from app.core.security import create_password_reset_token, verify_password_reset_token
from app.services.user_service import UserService

logger = structlog.get_logger()


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_service = UserService(db)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Аутентификация пользователя по email и паролю"""
        try:
            user = await self.user_service.get_by_email(email)
            if not user:
                return None
            
            if not user.hashed_password:
                return None
            
            if not verify_password(password, user.hashed_password):
                return None
            
            if not user.is_active:
                return None
            
            return user
            
        except Exception as e:
            logger.error("Error authenticating user", email=email, error=str(e))
            return None
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Создание нового пользователя"""
        return await self.user_service.create_user(user_data)
    
    async def oauth_authenticate(self, provider: str, oauth_data: UserOAuth) -> User:
        """OAuth аутентификация"""
        try:
            if provider == "google":
                return await self._handle_google_oauth(oauth_data)
            elif provider == "telegram":
                return await self._handle_telegram_oauth(oauth_data)
            else:
                raise ValueError(f"Unsupported OAuth provider: {provider}")
                
        except Exception as e:
            logger.error("Error in OAuth authentication", provider=provider, error=str(e))
            raise
    
    async def _handle_google_oauth(self, oauth_data: UserOAuth) -> User:
        """Обработка Google OAuth"""
        try:
            # Извлечение данных из Google токена
            google_user_data = oauth_data.user_data
            
            email = google_user_data.get("email")
            if not email:
                raise ValueError("Email not provided in Google OAuth data")
            
            # Проверка существования пользователя
            user = await self.user_service.get_by_email(email)
            
            if user:
                # Пользователь существует, обновляем OAuth данные
                if not user.oauth_provider or user.oauth_provider != "google":
                    await self._update_user_oauth(user.id, "google", google_user_data)
                return user
            
            # Создание нового пользователя
            username = google_user_data.get("given_name", "").lower()
            if not username:
                username = email.split("@")[0]
            
            # Генерация уникального username
            username = await self._generate_unique_username(username)
            
            user_data = UserCreate(
                email=email,
                username=username,
                password="",  # Пароль не нужен для OAuth
                first_name=google_user_data.get("given_name"),
                last_name=google_user_data.get("family_name"),
                oauth_provider="google",
                oauth_id=google_user_data.get("sub")
            )
            
            user = await self.user_service.create_user(user_data)
            await self._update_user_oauth(user.id, "google", google_user_data)
            
            return user
            
        except Exception as e:
            logger.error("Error handling Google OAuth", error=str(e))
            raise
    
    async def _handle_telegram_oauth(self, oauth_data: UserOAuth) -> User:
        """Обработка Telegram OAuth"""
        try:
            telegram_user_data = oauth_data.user_data
            
            telegram_id = telegram_user_data.get("id")
            if not telegram_id:
                raise ValueError("Telegram ID not provided in OAuth data")
            
            # Проверка существования пользователя
            user = await self.user_service.get_by_telegram_id(str(telegram_id))
            
            if user:
                # Пользователь существует, обновляем данные
                await self._update_user_telegram(user.id, telegram_user_data)
                return user
            
            # Создание нового пользователя
            username = telegram_user_data.get("username")
            if not username:
                username = f"user_{telegram_id}"
            
            # Генерация уникального username
            username = await self._generate_unique_username(username)
            
            user_data = UserCreate(
                email=f"telegram_{telegram_id}@telegram.local",  # Временный email
                username=username,
                password="",  # Пароль не нужен для OAuth
                first_name=telegram_user_data.get("first_name"),
                last_name=telegram_user_data.get("last_name"),
                oauth_provider="telegram",
                oauth_id=str(telegram_id)
            )
            
            user = await self.user_service.create_user(user_data)
            await self._update_user_telegram(user.id, telegram_user_data)
            
            return user
            
        except Exception as e:
            logger.error("Error handling Telegram OAuth", error=str(e))
            raise
    
    async def _update_user_oauth(self, user_id: str, provider: str, user_data: Dict[str, Any]) -> None:
        """Обновление OAuth данных пользователя"""
        try:
            update_data = {
                "oauth_provider": provider,
                "oauth_id": user_data.get("sub") or user_data.get("id")
            }
            
            await self.user_service.update_user(user_id, update_data)
            
        except Exception as e:
            logger.error("Error updating user OAuth data", user_id=user_id, provider=provider, error=str(e))
    
    async def _update_user_telegram(self, user_id: str, telegram_data: Dict[str, Any]) -> None:
        """Обновление Telegram данных пользователя"""
        try:
            update_data = {
                "telegram_id": str(telegram_data.get("id")),
                "telegram_username": telegram_data.get("username"),
                "first_name": telegram_data.get("first_name"),
                "last_name": telegram_data.get("last_name")
            }
            
            await self.user_service.update_user(user_id, update_data)
            
        except Exception as e:
            logger.error("Error updating user Telegram data", user_id=user_id, error=str(e))
    
    async def _generate_unique_username(self, base_username: str) -> str:
        """Генерация уникального username"""
        username = base_username
        counter = 1
        
        while await self.user_service.get_by_username(username):
            username = f"{base_username}_{counter}"
            counter += 1
        
        return username
    
    async def verify_password(self, user_id: str, password: str) -> bool:
        """Проверка пароля пользователя"""
        return await self.user_service.verify_user_password(user_id, password)
    
    async def change_password(self, user_id: str, new_password: str) -> bool:
        """Изменение пароля пользователя"""
        return await self.user_service.change_password(user_id, new_password)
    
    async def update_last_login(self, user_id: str) -> bool:
        """Обновление времени последнего входа"""
        return await self.user_service.update_last_login(user_id)
    
    async def create_password_reset_token(self, email: str) -> Optional[str]:
        """Создание токена для сброса пароля"""
        try:
            user = await self.user_service.get_by_email(email)
            if not user:
                return None
            
            # Создание токена
            token = create_password_reset_token(email)
            
            # Сохранение токена в Redis или БД (для отзыва)
            # Здесь можно добавить логику сохранения токена
            
            logger.info("Password reset token created", email=email)
            return token
            
        except Exception as e:
            logger.error("Error creating password reset token", email=email, error=str(e))
            return None
    
    async def confirm_password_reset(self, token: str, new_password: str) -> bool:
        """Подтверждение сброса пароля"""
        try:
            # Проверка токена
            email = verify_password_reset_token(token)
            if not email:
                return False
            
            # Получение пользователя
            user = await self.user_service.get_by_email(email)
            if not user:
                return False
            
            # Изменение пароля
            success = await self.user_service.change_password(str(user.id), new_password)
            
            if success:
                logger.info("Password reset confirmed", email=email)
            
            return success
            
        except Exception as e:
            logger.error("Error confirming password reset", error=str(e))
            return False
    
    async def connect_telegram(self, user_id: str, telegram_data: TelegramConnect) -> bool:
        """Подключение Telegram аккаунта"""
        try:
            # Проверка, что Telegram ID не занят
            existing_user = await self.user_service.get_by_telegram_id(telegram_data.telegram_id)
            if existing_user and str(existing_user.id) != user_id:
                return False
            
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
            
            user = await self.user_service.update_user(user_id, update_data)
            return user is not None
            
        except Exception as e:
            logger.error("Error connecting Telegram", user_id=user_id, error=str(e))
            return False
    
    async def disconnect_telegram(self, user_id: str) -> bool:
        """Отключение Telegram аккаунта"""
        try:
            update_data = {
                "telegram_id": None,
                "telegram_username": None,
                "telegram_notifications": False
            }
            
            user = await self.user_service.update_user(user_id, update_data)
            return user is not None
            
        except Exception as e:
            logger.error("Error disconnecting Telegram", user_id=user_id, error=str(e))
            return False
    
    async def verify_email(self, token: str) -> bool:
        """Подтверждение email"""
        try:
            from app.core.security import verify_email_verification_token
            
            email = verify_email_verification_token(token)
            if not email:
                return False
            
            user = await self.user_service.get_by_email(email)
            if not user:
                return False
            
            # Обновление статуса верификации
            update_data = {"is_verified": True}
            updated_user = await self.user_service.update_user(str(user.id), update_data)
            
            success = updated_user is not None
            if success:
                logger.info("Email verified", email=email)
            
            return success
            
        except Exception as e:
            logger.error("Error verifying email", error=str(e))
            return False
    
    async def create_email_verification_token(self, email: str) -> Optional[str]:
        """Создание токена для подтверждения email"""
        try:
            from app.core.security import create_email_verification_token
            
            user = await self.user_service.get_by_email(email)
            if not user:
                return None
            
            token = create_email_verification_token(email)
            
            logger.info("Email verification token created", email=email)
            return token
            
        except Exception as e:
            logger.error("Error creating email verification token", email=email, error=str(e))
            return None 