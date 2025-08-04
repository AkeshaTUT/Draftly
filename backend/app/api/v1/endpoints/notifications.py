from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_notifications():
    """Получение уведомлений"""
    return {"message": "Get notifications - to be implemented"}

@router.put("/{notification_id}/read")
async def mark_as_read(notification_id: str):
    """Отметить уведомление как прочитанное"""
    return {"message": f"Mark notification {notification_id} as read - to be implemented"}

@router.put("/read-all")
async def mark_all_as_read():
    """Отметить все уведомления как прочитанные"""
    return {"message": "Mark all notifications as read - to be implemented"}

@router.delete("/{notification_id}")
async def delete_notification(notification_id: str):
    """Удалить уведомление"""
    return {"message": f"Delete notification {notification_id} - to be implemented"} 