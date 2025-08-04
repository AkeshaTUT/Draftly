from celery import shared_task
import structlog

logger = structlog.get_logger()

@shared_task
def process_crypto_payment_task(payment_id: str):
    """Обработка криптоплатежа"""
    logger.info(f"Processing crypto payment {payment_id}")
    return {"status": "success", "payment_id": payment_id}

@shared_task
def process_yoomoney_payment_task(payment_id: str):
    """Обработка YooMoney платежа"""
    logger.info(f"Processing YooMoney payment {payment_id}")
    return {"status": "success", "payment_id": payment_id}

@shared_task
def process_kaspi_payment_task(payment_id: str):
    """Обработка Kaspi платежа"""
    logger.info(f"Processing Kaspi payment {payment_id}")
    return {"status": "success", "payment_id": payment_id} 