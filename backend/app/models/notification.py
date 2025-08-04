"""
Модель уведомления
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.core.database import Base

class NotificationType(str, enum.Enum):
    """Типы уведомлений"""
    COMMENT = "comment"
    LIKE = "like"
    FOLLOW = "follow"
    MENTION = "mention"
    SYSTEM = "system"

class NotificationStatus(str, enum.Enum):
    """Статусы уведомления"""
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"

class Notification(Base):
    """Модель уведомления"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Основная информация
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False, index=True)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.UNREAD, index=True)
    
    # Связи
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Кто вызвал уведомление
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=True)  # Связанная статья
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)  # Связанный комментарий
    
    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    # Дополнительные данные
    data = Column(Text, nullable=True)  # JSON данные для дополнительной информации
    
    # Связи
    user = relationship("User", foreign_keys=[user_id])
    sender = relationship("User", foreign_keys=[sender_id])
    article = relationship("Article")
    comment = relationship("Comment")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type='{self.notification_type}')>"
    
    @property
    def is_read(self) -> bool:
        """Проверка, прочитано ли уведомление"""
        return self.status == NotificationStatus.READ
    
    def mark_as_read(self):
        """Отметить как прочитанное"""
        self.status = NotificationStatus.READ
        self.read_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Преобразование в словарь"""
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "notification_type": self.notification_type.value,
            "status": self.status.value,
            "is_read": self.is_read,
            "created_at": self.created_at,
            "read_at": self.read_at,
            "sender": self.sender.public_profile if self.sender else None,
            "article": {
                "id": self.article.id,
                "title": self.article.title,
                "slug": self.article.slug
            } if self.article else None,
            "comment": {
                "id": self.comment.id,
                "content": self.comment.content[:100] + "..." if len(self.comment.content) > 100 else self.comment.content
            } if self.comment else None
        }
