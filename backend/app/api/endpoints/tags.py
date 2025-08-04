"""
Tags endpoints
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_tags():
    """Получение тегов"""
    return {"message": "Tags endpoint - coming soon"}

@router.get("/{tag_slug}")
async def get_tag(tag_slug: str):
    """Получение тега по slug"""
    return {"message": f"Tag {tag_slug} - coming soon"}
