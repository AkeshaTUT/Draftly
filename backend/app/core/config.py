"""
Конфигурация приложения
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки
    PROJECT_NAME: str = "Teletype.in Analog"
    VERSION: str = "2.0.0"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # API настройки
    API_PREFIX: str = "/api"
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 дней
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 дней
    
    # База данных
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./analog_teletype.db", env="DATABASE_URL")
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    REDIS_CACHE_TTL: int = 3600  # 1 час
    
    # Celery
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379", env="CELERY_BROKER_URL")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        env="CORS_ORIGINS"
    )
    
    # Загрузка файлов
    UPLOADS_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    
    # Email настройки
    SMTP_TLS: bool = Field(default=True, env="SMTP_TLS")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_HOST: str = Field(default="", env="SMTP_HOST")
    SMTP_USER: str = Field(default="", env="SMTP_USER")
    SMTP_PASSWORD: str = Field(default="", env="SMTP_PASSWORD")
    EMAILS_FROM_EMAIL: str = Field(default="", env="EMAILS_FROM_EMAIL")
    EMAILS_FROM_NAME: str = Field(default="Teletype.in Analog", env="EMAILS_FROM_NAME")
    
    # Telegram бот
    TELEGRAM_BOT_TOKEN: str = Field(default="", env="TELEGRAM_BOT_TOKEN")
    TELEGRAM_WEBHOOK_URL: str = Field(default="", env="TELEGRAM_WEBHOOK_URL")
    
    # OAuth
    GOOGLE_CLIENT_ID: str = Field(default="", env="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = Field(default="", env="GOOGLE_CLIENT_SECRET")
    
    # Безопасность
    BCRYPT_ROUNDS: int = 12
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Аналитика и мониторинг
    SENTRY_DSN: str = Field(default="", env="SENTRY_DSN")
    
    # Донаты
    YOOMONEY_WALLET: str = Field(default="", env="YOOMONEY_WALLET")
    CRYPTO_WALLET_BTC: str = Field(default="", env="CRYPTO_WALLET_BTC")
    CRYPTO_WALLET_ETH: str = Field(default="", env="CRYPTO_WALLET_ETH")
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    @validator("UPLOADS_DIR", pre=True)
    def create_uploads_dir(cls, v):
        uploads_path = Path(v)
        uploads_path.mkdir(exist_ok=True)
        return str(uploads_path)
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Игнорировать дополнительные поля

# Создание экземпляра настроек
settings = Settings()
