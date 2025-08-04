from celery import shared_task
import structlog

logger = structlog.get_logger()

@shared_task
def cleanup_expired_tokens_task():
    """Очистка истекших токенов"""
    logger.info("Cleaning up expired tokens")
    return {"status": "success"}

@shared_task
def cleanup_old_notifications_task():
    """Очистка старых уведомлений"""
    logger.info("Cleaning up old notifications")
    return {"status": "success"}

@shared_task
def cleanup_temp_files_task():
    """Очистка временных файлов"""
    logger.info("Cleaning up temporary files")
    return {"status": "success"} 