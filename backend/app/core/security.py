"""
Безопасность и аутентификация
"""

from datetime import datetime, timedelta
from typing import Any, Optional
from fastapi import HTTPException, status, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.hash import bcrypt

from app.core.config import settings

# Контекст для работы с паролями
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer токен схема
security = HTTPBearer()

class SecurityUtils:
    """Утилиты для безопасности"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Проверка пароля"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Хеширование пароля"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(
        subject: Any, 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Создание access токена"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm="HS256"
        )
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(subject: Any) -> str:
        """Создание refresh токена"""
        expire = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm="HS256"
        )
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Optional[str]:
        """Проверка токена"""
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=["HS256"]
            )
            
            # Проверка типа токена
            if payload.get("type") != token_type:
                return None
                
            # Проверка срока действия
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
                return None
                
            return payload.get("sub")
            
        except JWTError:
            return None
    
    @staticmethod
    def generate_password_reset_token(email: str) -> str:
        """Генерация токена для сброса пароля"""
        delta = timedelta(hours=24)  # Токен действует 24 часа
        now = datetime.utcnow()
        expires = now + delta
        
        exp = expires.timestamp()
        encoded_jwt = jwt.encode(
            {"exp": exp, "nbf": now, "sub": email, "type": "password_reset"},
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return encoded_jwt
    
    @staticmethod
    def verify_password_reset_token(token: str) -> Optional[str]:
        """Проверка токена сброса пароля"""
        try:
            decoded_token = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=["HS256"]
            )
            
            if decoded_token.get("type") != "password_reset":
                return None
                
            return decoded_token.get("sub")
            
        except JWTError:
            return None

def setup_security_headers(response: Response) -> Response:
    """Настройка заголовков безопасности"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    
    # Content Security Policy
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self' ws: wss:; "
        "frame-ancestors 'none'"
    )
    response.headers["Content-Security-Policy"] = csp
    
    return response

# Инициализация утилит безопасности
security_utils = SecurityUtils()

# Простые заглушки для функций аутентификации
async def get_current_user():
    """Заглушка для получения текущего пользователя"""
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required"
    )


async def get_current_active_user():
    """Заглушка для получения активного пользователя"""
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Active user required"
    )


async def get_current_admin_user():
    """Заглушка для получения администратора"""
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin access required"
    )


async def get_current_moderator_user():
    """Заглушка для получения модератора"""
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Moderator access required"
    )


# Функции-обёртки для удобства
def create_access_token(subject: Any, expires_delta: Optional[timedelta] = None) -> str:
    """Создание access токена"""
    return SecurityUtils.create_access_token(subject, expires_delta)


def create_refresh_token(subject: Any) -> str:
    """Создание refresh токена"""
    return SecurityUtils.create_refresh_token(subject)


def create_password_reset_token(email: str) -> str:
    """Создание токена для сброса пароля"""
    return SecurityUtils.generate_password_reset_token(email)


def verify_password_reset_token(token: str) -> Optional[str]:
    """Проверка токена сброса пароля"""
    return SecurityUtils.verify_password_reset_token(token)
