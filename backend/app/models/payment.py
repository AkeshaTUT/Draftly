from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
import json

from app.core.database import Base


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentMethod(str, enum.Enum):
    CRYPTO = "crypto"
    YOOMONEY = "yoomoney"
    KASPI = "kaspi"
    TELEGRAM = "telegram"


class PaymentType(str, enum.Enum):
    DONATION = "donation"
    SUBSCRIPTION = "subscription"
    PREMIUM = "premium"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    
    # Пользователи
    user_id = Column(Integer, nullable=False, index=True)  # Кто платит
    recipient_id = Column(Integer, nullable=False, index=True)  # Кому платят
    
    # Сумма и валюта
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="RUB")  # RUB, USD, EUR
    
    # Тип и метод платежа
    payment_type = Column(Enum(PaymentType), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    
    # Статус
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    
    # Внешние ID платежных систем
    external_payment_id = Column(String(255), nullable=True, index=True)
    external_transaction_id = Column(String(255), nullable=True)
    
    # Описание
    description = Column(Text, nullable=True)
    message = Column(Text, nullable=True)  # Сообщение от донатера
    
    # Связанная статья (для донатов к статье)
    article_id = Column(Integer, nullable=True, index=True)
    
    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Дополнительные данные
    _payment_metadata = Column("payment_metadata", Text, default="{}")
    
    # Связи
    user = relationship("User", foreign_keys=[user_id], back_populates="payments")
    recipient = relationship("User", foreign_keys=[recipient_id])
    article = relationship("Article")
    
    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount}, status={self.status})>"
    
    @property
    def is_completed(self) -> bool:
        """Проверка завершения платежа"""
        return self.status == PaymentStatus.COMPLETED
    
    @property
    def is_pending(self) -> bool:
        """Проверка ожидания платежа"""
        return self.status == PaymentStatus.PENDING
    
    @property
    def payment_metadata(self) -> dict:
        """Получение метаданных платежа"""
        try:
            return json.loads(self._payment_metadata)
        except (json.JSONDecodeError, TypeError):
            return {}
    
    @payment_metadata.setter
    def payment_metadata(self, value: dict):
        """Установка метаданных платежа"""
        self._payment_metadata = json.dumps(value)


class CryptoPayment(Base):
    __tablename__ = "crypto_payments"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, nullable=False, index=True)
    
    # Криптовалюта
    cryptocurrency = Column(String(10), nullable=False)  # BTC, ETH, USDT, etc.
    wallet_address = Column(String(255), nullable=False)
    
    # Сумма в криптовалюте
    crypto_amount = Column(Float, nullable=False)
    
    # Курс обмена
    exchange_rate = Column(Float, nullable=True)
    
    # Статус блокчейна
    blockchain_status = Column(String(50), nullable=True)
    transaction_hash = Column(String(255), nullable=True)
    block_number = Column(Integer, nullable=True)
    
    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связи
    payment = relationship("Payment")
    
    def __repr__(self):
        return f"<CryptoPayment(id={self.id}, crypto={self.cryptocurrency}, amount={self.crypto_amount})>"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    subscriber_id = Column(Integer, nullable=False, index=True)
    
    # Тип подписки
    subscription_type = Column(String(50), nullable=False)  # monthly, yearly, etc.
    
    # Сумма
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="RUB")
    
    # Период
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    
    # Статус
    is_active = Column(Boolean, default=True)
    auto_renew = Column(Boolean, default=True)
    
    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связи
    user = relationship("User", foreign_keys=[user_id])
    subscriber = relationship("User", foreign_keys=[subscriber_id])
    
    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, subscriber_id={self.subscriber_id})>"
    
    @property
    def is_expired(self) -> bool:
        """Проверка истечения подписки"""
        if not self.end_date:
            return False
        from datetime import datetime
        return datetime.utcnow() > self.end_date 