# Импорт всех сервисов
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.email_service import EmailService

# Экспорт всех сервисов
__all__ = [
    "UserService",
    "AuthService", 
    "EmailService",
] 