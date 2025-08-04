from celery import Celery
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Создание Celery приложения
celery_app = Celery(
    "analog_teletype",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.email_tasks",
        "app.tasks.notification_tasks",
        "app.tasks.article_tasks",
        "app.tasks.payment_tasks",
    ]
)

# Конфигурация Celery
celery_app.conf.update(
    # Основные настройки
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Настройки задач
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 минут
    task_soft_time_limit=25 * 60,  # 25 минут
    
    # Настройки воркера
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    
    # Настройки планировщика
    beat_schedule={
        "cleanup-expired-tokens": {
            "task": "app.tasks.cleanup_tasks.cleanup_expired_tokens",
            "schedule": 3600.0,  # каждый час
        },
        "update-article-stats": {
            "task": "app.tasks.article_tasks.update_article_statistics",
            "schedule": 300.0,  # каждые 5 минут
        },
        "send-daily-digest": {
            "task": "app.tasks.notification_tasks.send_daily_digest",
            "schedule": 86400.0,  # каждый день в 9:00
        },
    },
    
    # Настройки результатов
    result_expires=3600,  # 1 час
    
    # Настройки очередей
    task_default_queue="default",
    task_queues={
        "default": {
            "exchange": "default",
            "routing_key": "default",
        },
        "email": {
            "exchange": "email",
            "routing_key": "email",
        },
        "notifications": {
            "exchange": "notifications",
            "routing_key": "notifications",
        },
        "payments": {
            "exchange": "payments",
            "routing_key": "payments",
        },
    },
    
    # Настройки роутинга
    task_routes={
        "app.tasks.email_tasks.*": {"queue": "email"},
        "app.tasks.notification_tasks.*": {"queue": "notifications"},
        "app.tasks.payment_tasks.*": {"queue": "payments"},
    },
)

# Обработчики событий Celery
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    logger.info("Celery periodic tasks configured")


@celery_app.task(bind=True)
def debug_task(self):
    logger.info(f"Request: {self.request!r}")


# Функция для получения Celery приложения
def get_celery_app():
    return celery_app 