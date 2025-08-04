"""
Notifications endpoints
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_notifications():
    """Получение уведомлений"""
    return {"message": "Notifications endpoint - coming soon"}

@router.patch("/{notification_id}/read")
async def mark_notification_read(notification_id: int):
    """Отметить уведомление как прочитанное"""
    return {"message": f"Mark notification {notification_id} as read - coming soon"}
