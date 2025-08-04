"""
Files endpoints
"""

from fastapi import APIRouter

router = APIRouter()

@router.post("/upload")
async def upload_file():
    """Загрузка файла"""
    return {"message": "File upload - coming soon"}

@router.get("/{file_id}")
async def get_file(file_id: str):
    """Получение файла"""
    return {"message": f"File {file_id} - coming soon"}
