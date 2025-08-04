from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    articles,
    comments,
    interactions,
    payments,
    notifications,
    search,
    uploads,
    admin
)

api_router = APIRouter()

# Аутентификация
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

# Пользователи
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

# Статьи
api_router.include_router(
    articles.router,
    prefix="/articles",
    tags=["articles"]
)

# Комментарии
api_router.include_router(
    comments.router,
    prefix="/comments",
    tags=["comments"]
)

# Взаимодействия (лайки, закладки, подписки)
api_router.include_router(
    interactions.router,
    prefix="/interactions",
    tags=["interactions"]
)

# Платежи и донаты
api_router.include_router(
    payments.router,
    prefix="/payments",
    tags=["payments"]
)

# Уведомления
api_router.include_router(
    notifications.router,
    prefix="/notifications",
    tags=["notifications"]
)

# Поиск
api_router.include_router(
    search.router,
    prefix="/search",
    tags=["search"]
)

# Загрузка файлов
api_router.include_router(
    uploads.router,
    prefix="/uploads",
    tags=["uploads"]
)

# Административные функции
api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"]
) 