"""
Comments endpoints
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_comments():
    """Получение комментариев"""
    return {"message": "Comments endpoint - coming soon"}

@router.post("/")
async def create_comment():
    """Создание комментария"""
    return {"message": "Create comment - coming soon"}
