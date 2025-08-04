"""
Схемы для аутентификации
"""

from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
import re

class UserCreate(BaseModel):
    """Схема создания пользователя"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    display_name: Optional[str] = Field(None, max_length=100)
    
    @validator("username")
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Username can only contain letters, numbers, underscores and hyphens")
        if v.lower() in ["admin", "api", "www", "mail", "ftp", "root", "support"]:
            raise ValueError("This username is reserved")
        return v.lower()
    
    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v

class UserLogin(BaseModel):
    """Схема входа в систему"""
    email: EmailStr
    password: str
    remember_me: Optional[bool] = False

class TokenResponse(BaseModel):
    """Схема ответа с токеном"""
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None

class PasswordReset(BaseModel):
    """Схема запроса сброса пароля"""
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """Схема подтверждения сброса пароля"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @validator("new_password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v

class ChangePassword(BaseModel):
    """Схема смены пароля"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @validator("new_password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v
