"""
Основной API роутер
"""

from fastapi import APIRouter
from app.api.endpoints import auth, users, articles, comments, tags, notifications, files

api_router = APIRouter()

# Подключение всех эндпоинтов
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
