# Импорт всех задач
from app.tasks.email_tasks import (
    send_welcome_email_task,
    send_password_reset_email_task,
    send_notification_email_task
)
from app.tasks.notification_tasks import (
    send_telegram_notification_task,
    send_daily_digest_task,
    create_notification_task
)
from app.tasks.article_tasks import (
    update_article_statistics_task,
    generate_article_preview_task,
    process_markdown_task
)
from app.tasks.payment_tasks import (
    process_crypto_payment_task,
    process_yoomoney_payment_task,
    process_kaspi_payment_task
)
from app.tasks.cleanup_tasks import (
    cleanup_expired_tokens_task,
    cleanup_old_notifications_task,
    cleanup_temp_files_task
)

# Экспорт всех задач
__all__ = [
    # Email tasks
    "send_welcome_email_task",
    "send_password_reset_email_task", 
    "send_notification_email_task",
    
    # Notification tasks
    "send_telegram_notification_task",
    "send_daily_digest_task",
    "create_notification_task",
    
    # Article tasks
    "update_article_statistics_task",
    "generate_article_preview_task",
    "process_markdown_task",
    
    # Payment tasks
    "process_crypto_payment_task",
    "process_yoomoney_payment_task",
    "process_kaspi_payment_task",
    
    # Cleanup tasks
    "cleanup_expired_tokens_task",
    "cleanup_old_notifications_task",
    "cleanup_temp_files_task",
] 