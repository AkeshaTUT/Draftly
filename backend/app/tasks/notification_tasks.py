from celery import shared_task
import structlog

logger = structlog.get_logger()

@shared_task
def send_telegram_notification_task(telegram_id: str, message: str):
    """Отправка уведомления в Telegram"""
    logger.info(f"Sending Telegram notification to {telegram_id}")
    return {"status": "success", "telegram_id": telegram_id}

@shared_task
def send_daily_digest_task():
    """Отправка ежедневного дайджеста"""
    logger.info("Sending daily digest")
    return {"status": "success"}

@shared_task
def create_notification_task(user_id: str, notification_type: str, data: dict):
    """Создание уведомления"""
    logger.info(f"Creating notification for user {user_id}")
    return {"status": "success", "user_id": user_id} 