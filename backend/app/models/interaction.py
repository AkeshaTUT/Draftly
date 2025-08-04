from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
import json

from app.core.database import Base


class CommentStatus(str, enum.Enum):
    ACTIVE = "active"
    HIDDEN = "hidden"
    DELETED = "deleted"


class NotificationType(str, enum.Enum):
    COMMENT = "comment"
    LIKE = "like"
    FOLLOW = "follow"
    MENTION = "mention"
    ARTICLE_PUBLISHED = "article_published"
    PAYMENT_RECEIVED = "payment_received"
    SYSTEM = "system"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    
    # Автор
    author_id = Column(Integer, nullable=False, index=True)
    
    # Статья
    article_id = Column(Integer, nullable=False, index=True)
    
    # Родительский комментарий (для вложенных комментариев)
    parent_id = Column(Integer, nullable=True, index=True)
    
    # Статус
    status = Column(Enum(CommentStatus), default=CommentStatus.ACTIVE)
    
    # Статистика
    like_count = Column(Integer, default=0)
    reply_count = Column(Integer, default=0)
    
    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Дополнительные данные
    _comment_metadata = Column("comment_metadata", Text, default="{}")
    
    # Связи
    author = relationship("User", back_populates="comments")
    article = relationship("Article", back_populates="comments")
    parent = relationship("Comment", remote_side=[id])
    replies = relationship("Comment", back_populates="parent")
    likes = relationship("CommentLike", back_populates="comment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Comment(id={self.id}, author_id={self.author_id}, article_id={self.article_id})>"


class CommentLike(Base):
    __tablename__ = "comment_likes"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    comment = relationship("Comment", back_populates="likes")
    user = relationship("User")


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    article = relationship("Article", back_populates="likes")
    user = relationship("User", back_populates="likes")
    
    def __repr__(self):
        return f"<Like(id={self.id}, user_id={self.user_id}, article_id={self.article_id})>"


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    article = relationship("Article", back_populates="bookmarks")
    user = relationship("User", back_populates="bookmarks")
    
    def __repr__(self):
        return f"<Bookmark(id={self.id}, user_id={self.user_id}, article_id={self.article_id})>"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Тип уведомления
    type = Column(Enum(NotificationType), nullable=False)
    
    # Заголовок и сообщение
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    
    # Ссылка на связанный объект
    target_type = Column(String(50), nullable=True)  # article, comment, user, etc.
    target_id = Column(Integer, nullable=True)
    
    # Статус
    is_read = Column(Boolean, default=False)
    is_sent_email = Column(Boolean, default=False)
    is_sent_telegram = Column(Boolean, default=False)
    
    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    # Дополнительные данные
    _data = Column("data", Text, default="{}")
    
    # Связи
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.type})>"
    
    @property
    def target_url(self) -> str:
        """URL для перехода к уведомлению"""
        if self.target_type == "article" and self.target_id:
            return f"/article/{self.target_id}"
        elif self.target_type == "user" and self.target_id:
            return f"/user/{self.target_id}"
        return "#" 