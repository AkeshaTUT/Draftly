"""
Celery для фоновых задач
"""

from celery import Celery
from app.core.config import settings

# Создание Celery приложения
celery = Celery(
    "teletype_analog",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.email_tasks", "app.tasks.notification_tasks"]
)

# Конфигурация Celery
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 минут
    task_soft_time_limit=25 * 60,  # 25 минут
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)

# Периодические задачи
celery.conf.beat_schedule = {
    "cleanup-expired-tokens": {
        "task": "app.tasks.cleanup_tasks.cleanup_expired_tokens",
        "schedule": 3600.0,  # Каждый час
    },
    "send-digest-emails": {
        "task": "app.tasks.email_tasks.send_digest_emails", 
        "schedule": 86400.0,  # Каждый день
    },
}
