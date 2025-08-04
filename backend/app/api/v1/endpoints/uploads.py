from fastapi import APIRouter

router = APIRouter()

@router.post("/image")
async def upload_image():
    """Загрузка изображения"""
    return {"message": "Upload image - to be implemented"}

@router.post("/avatar")
async def upload_avatar():
    """Загрузка аватара"""
    return {"message": "Upload avatar - to be implemented"}

@router.delete("/{file_id}")
async def delete_file(file_id: str):
    """Удаление файла"""
    return {"message": f"Delete file {file_id} - to be implemented"} 