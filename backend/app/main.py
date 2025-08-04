"""
FastAPI приложение - профессиональный аналог Teletype.in
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import structlog

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import engine, Base

# Настройка логирования
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

# Создание приложения
app = FastAPI(
    title="Teletype.in Analog API",
    description="Современная блог-платформа с расширенными возможностями",
    version="2.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    openapi_url="/openapi.json" if settings.ENVIRONMENT == "development" else None,
)

# Инициализация базы данных
@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске приложения"""
    logger.info("Starting Teletype.in Analog API", version="2.0.0")
    
    # Создание таблиц (в продакшене используйте Alembic)
    if settings.ENVIRONMENT == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")

@app.on_event("shutdown")
async def shutdown_event():
    """Очистка при завершении приложения"""
    logger.info("Shutting down Teletype.in Analog API")

# Middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Middleware для доверенных хостов
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.ENVIRONMENT == "development" else ["api.yourdomain.com"]
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Настройка заголовков безопасности
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    # Add basic security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        "Request processed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=round(process_time, 4),
        client_ip=get_remote_address(request)
    )
    
    return response

# Статические файлы (загрузки)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# API маршруты
app.include_router(api_router, prefix="/api")

# Корневой маршрут
@app.get("/")
async def root():
    """Корневая страница API"""
    return {
        "message": "Teletype.in Analog API",
        "version": "2.0.0",
        "status": "active",
        "docs": "/docs" if settings.ENVIRONMENT == "development" else "Documentation not available in production",
        "features": [
            "User authentication & profiles",
            "Article creation & editing", 
            "Markdown support",
            "Real-time comments",
            "File uploads",
            "PWA support",
            "Telegram notifications",
            "Security & rate limiting"
        ]
    }

# Проверка здоровья приложения
@app.get("/health")
async def health_check():
    """Проверка состояния приложения"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "environment": settings.ENVIRONMENT,
        "database": "connected",  # TODO: добавить реальную проверку БД
        "redis": "connected"       # TODO: добавить реальную проверку Redis
    }

# Обработка ошибок
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error("Internal server error", error=str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

import time
