from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_comments():
    """Получение списка комментариев"""
    return {"message": "Comments endpoint - to be implemented"}

@router.post("/")
async def create_comment():
    """Создание нового комментария"""
    return {"message": "Create comment endpoint - to be implemented"}

@router.get("/{comment_id}")
async def get_comment(comment_id: str):
    """Получение комментария по ID"""
    return {"message": f"Get comment {comment_id} - to be implemented"}

@router.put("/{comment_id}")
async def update_comment(comment_id: str):
    """Обновление комментария"""
    return {"message": f"Update comment {comment_id} - to be implemented"}

@router.delete("/{comment_id}")
async def delete_comment(comment_id: str):
    """Удаление комментария"""
    return {"message": f"Delete comment {comment_id} - to be implemented"} 