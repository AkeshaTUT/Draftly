from fastapi import APIRouter

router = APIRouter()

@router.get("/articles")
async def search_articles():
    """Поиск статей"""
    return {"message": "Search articles - to be implemented"}

@router.get("/users")
async def search_users():
    """Поиск пользователей"""
    return {"message": "Search users - to be implemented"}

@router.get("/tags")
async def search_tags():
    """Поиск тегов"""
    return {"message": "Search tags - to be implemented"} 