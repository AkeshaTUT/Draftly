from passlib.context import CryptContext
from pydantic import ValidationError
import re

# Создаем контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хеширование пароля"""
    return pwd_context.hash(password)


def validate_password_strength(password: str) -> bool:
    """
    Валидация сложности пароля
    """
    if len(password) < 8:
        return False
    
    # Проверяем наличие заглавных букв
    if not re.search(r'[A-Z]', password):
        return False
    
    # Проверяем наличие строчных букв
    if not re.search(r'[a-z]', password):
        return False
    
    # Проверяем наличие цифр
    if not re.search(r'\d', password):
        return False
    
    # Проверяем наличие специальных символов
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    return True 