"""
Сервис для работы с пользователями
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import update
from datetime import datetime
from typing import Optional, List

from app.models.user import User, UserRole
from app.schemas.auth import UserCreate
from app.core.security import security_utils
import structlog

logger = structlog.get_logger()

class UserService:
    """Сервис для работы с пользователями"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Получение пользователя по ID"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Получение пользователя по email"""
        result = await self.db.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Получение пользователя по username"""
        result = await self.db.execute(
            select(User).where(User.username == username.lower())
        )
        return result.scalar_one_or_none()
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Создание нового пользователя"""
        hashed_password = security_utils.get_password_hash(user_data.password)
        
        user = User(
            username=user_data.username.lower(),
            email=user_data.email.lower(),
            hashed_password=hashed_password,
            display_name=user_data.display_name or user_data.username,
            is_active=True,
            is_verified=False,
            role=UserRole.USER
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        logger.info("User created", user_id=user.id, username=user.username)
        return user
    
    async def update_password(self, user_id: int, new_password: str) -> bool:
        """Обновление пароля пользователя"""
        hashed_password = security_utils.get_password_hash(new_password)
        
        result = await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(hashed_password=hashed_password)
        )
        
        await self.db.commit()
        
        logger.info("Password updated", user_id=user_id)
        return result.rowcount > 0
    
    async def update_last_login(self, user_id: int) -> bool:
        """Обновление времени последнего входа"""
        result = await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(last_login=datetime.utcnow())
        )
        
        await self.db.commit()
        return result.rowcount > 0
    
    async def verify_user(self, user_id: int) -> bool:
        """Верификация пользователя"""
        result = await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_verified=True)
        )
        
        await self.db.commit()
        
        logger.info("User verified", user_id=user_id)
        return result.rowcount > 0
    
    async def deactivate_user(self, user_id: int) -> bool:
        """Деактивация пользователя"""
        result = await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_active=False)
        )
        
        await self.db.commit()
        
        logger.info("User deactivated", user_id=user_id)
        return result.rowcount > 0
    
    async def get_users_by_role(self, role: UserRole) -> List[User]:
        """Получение пользователей по роли"""
        result = await self.db.execute(
            select(User).where(User.role == role)
        )
        return result.scalars().all()
    
    async def search_users(self, query: str, limit: int = 10) -> List[User]:
        """Поиск пользователей"""
        result = await self.db.execute(
            select(User)
            .where(
                (User.username.ilike(f"%{query}%")) |
                (User.display_name.ilike(f"%{query}%"))
            )
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_user_stats(self, user_id: int) -> dict:
        """Получение статистики пользователя"""
        user = await self.get_by_id(user_id)
        if not user:
            return {}
        
        return {
            "articles_count": user.articles_count,
            "followers_count": user.followers_count,
            "following_count": user.following_count,
            "created_at": user.created_at,
            "last_login": user.last_login
        }
