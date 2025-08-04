"""
Users endpoints
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_users():
    """Получение списка пользователей"""
    return {"message": "Users endpoint - coming soon"}

@router.get("/{username}")
async def get_user_profile(username: str):
    """Получение профиля пользователя"""
    return {"message": f"User profile for {username} - coming soon"}
