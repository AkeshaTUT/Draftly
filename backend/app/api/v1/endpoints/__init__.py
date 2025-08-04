# Импорт всех роутеров
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

# Экспорт всех роутеров
__all__ = [
    "auth",
    "users", 
    "articles",
    "comments",
    "interactions",
    "payments",
    "notifications",
    "search",
    "uploads",
    "admin",
] 