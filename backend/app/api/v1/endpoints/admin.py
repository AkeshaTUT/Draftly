from fastapi import APIRouter

router = APIRouter()

@router.get("/stats")
async def get_stats():
    """Получение статистики"""
    return {"message": "Get stats - to be implemented"}

@router.get("/users")
async def admin_get_users():
    """Получение списка пользователей для админа"""
    return {"message": "Admin get users - to be implemented"}

@router.put("/users/{user_id}/ban")
async def ban_user(user_id: str):
    """Бан пользователя"""
    return {"message": f"Ban user {user_id} - to be implemented"}

@router.put("/users/{user_id}/unban")
async def unban_user(user_id: str):
    """Разбан пользователя"""
    return {"message": f"Unban user {user_id} - to be implemented"}

@router.put("/articles/{article_id}/feature")
async def feature_article(article_id: str):
    """Выделить статью"""
    return {"message": f"Feature article {article_id} - to be implemented"} 