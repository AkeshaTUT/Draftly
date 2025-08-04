from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import datetime
import uuid

from app.models.user import UserRole, UserStatus


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=1000)
    website: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=100)
    is_public_profile: bool = True
    email_notifications: bool = True
    telegram_notifications: bool = False


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('password', mode='before')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=1000)
    avatar_url: Optional[str] = Field(None, max_length=500)
    website: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=100)
    is_public_profile: Optional[bool] = None
    email_notifications: Optional[bool] = None
    telegram_notifications: Optional[bool] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOAuth(BaseModel):
    provider: str = Field(..., pattern="^(google|telegram)$")
    token: str
    user_data: dict


class UserResponse(UserBase):
    id: uuid.UUID
    avatar_url: Optional[str] = None
    is_verified: bool
    role: UserRole
    status: UserStatus
    oauth_provider: Optional[str] = None
    telegram_id: Optional[str] = None
    telegram_username: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }


class UserProfile(UserResponse):
    """Расширенный профиль пользователя с дополнительной информацией"""
    followers_count: int = 0
    following_count: int = 0
    articles_count: int = 0
    total_views: int = 0
    total_likes: int = 0


class UserList(BaseModel):
    """Список пользователей для пагинации"""
    users: List[UserResponse]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('new_password', mode='before')
    @classmethod
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class PasswordReset(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('new_password', mode='before')
    @classmethod
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class TelegramConnect(BaseModel):
    telegram_id: str
    telegram_username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserPreferences(BaseModel):
    """Настройки пользователя"""
    theme: str = Field("light", pattern="^(light|dark|auto)$")
    language: str = Field("ru", pattern="^(ru|en)$")
    timezone: str = Field("UTC", max_length=50)
    email_digest: bool = True
    email_comments: bool = True
    email_likes: bool = True
    email_follows: bool = True
    telegram_digest: bool = False
    telegram_comments: bool = False
    telegram_likes: bool = False
    telegram_follows: bool = False 