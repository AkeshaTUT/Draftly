from celery import shared_task
import structlog

logger = structlog.get_logger()

@shared_task
def send_welcome_email_task(email: str, username: str):
    """Отправка приветственного email"""
    logger.info(f"Sending welcome email to {email}")
    return {"status": "success", "email": email}

@shared_task
def send_password_reset_email_task(email: str, reset_token: str):
    """Отправка email для сброса пароля"""
    logger.info(f"Sending password reset email to {email}")
    return {"status": "success", "email": email}

@shared_task
def send_notification_email_task(email: str, subject: str, message: str):
    """Отправка уведомления по email"""
    logger.info(f"Sending notification email to {email}")
    return {"status": "success", "email": email} 