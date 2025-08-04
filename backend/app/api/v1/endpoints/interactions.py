from fastapi import APIRouter

router = APIRouter()

@router.post("/like/{article_id}")
async def like_article(article_id: str):
    """Лайк статьи"""
    return {"message": f"Like article {article_id} - to be implemented"}

@router.delete("/like/{article_id}")
async def unlike_article(article_id: str):
    """Убрать лайк статьи"""
    return {"message": f"Unlike article {article_id} - to be implemented"}

@router.post("/bookmark/{article_id}")
async def bookmark_article(article_id: str):
    """Добавить статью в закладки"""
    return {"message": f"Bookmark article {article_id} - to be implemented"}

@router.delete("/bookmark/{article_id}")
async def unbookmark_article(article_id: str):
    """Убрать статью из закладок"""
    return {"message": f"Unbookmark article {article_id} - to be implemented"}

@router.get("/bookmarks")
async def get_bookmarks():
    """Получить закладки пользователя"""
    return {"message": "Get bookmarks - to be implemented"} 