"""
Articles endpoints
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_articles():
    """Получение списка статей"""
    return {"message": "Articles endpoint - coming soon"}

@router.post("/")
async def create_article():
    """Создание новой статьи"""
    return {"message": "Create article - coming soon"}

@router.get("/{article_id}")
async def get_article(article_id: int):
    """Получение статьи по ID"""
    return {"message": f"Article {article_id} - coming soon"}
