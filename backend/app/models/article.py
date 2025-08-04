"""
Модель статьи
"""

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, 
    ForeignKey, Enum, JSON, Index
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.core.database import Base

class ArticleStatus(str, enum.Enum):
    """Статусы статьи"""
    DRAFT = "draft"         # Черновик
    PUBLISHED = "published" # Опубликована
    ARCHIVED = "archived"   # Архивирована
    DELETED = "deleted"     # Удалена

class ArticleVisibility(str, enum.Enum):
    """Видимость статьи"""
    PUBLIC = "public"       # Публичная
    UNLISTED = "unlisted"   # Доступна по ссылке
    PRIVATE = "private"     # Приватная

class Article(Base):
    """Модель статьи"""
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Основная информация
    title = Column(String(200), nullable=False, index=True)
    slug = Column(String(250), unique=True, index=True, nullable=False)
    subtitle = Column(String(300), nullable=True)
    content = Column(Text, nullable=False)
    excerpt = Column(Text, nullable=True)  # Краткое описание
    
    # Мета-информация
    cover_image = Column(String(500), nullable=True)
    reading_time = Column(Integer, default=0)  # В минутах
    word_count = Column(Integer, default=0)
    
    # Статус и видимость
    status = Column(Enum(ArticleStatus), default=ArticleStatus.DRAFT, index=True)
    visibility = Column(Enum(ArticleVisibility), default=ArticleVisibility.PUBLIC, index=True)
    
    # Автор
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Даты
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True, index=True)
    
    # Статистика
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    
    # SEO
    meta_description = Column(String(160), nullable=True)
    meta_keywords = Column(String(255), nullable=True)
    canonical_url = Column(String(500), nullable=True)
    
    # Дополнительные настройки
    allow_comments = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_pinned = Column(Boolean, default=False)
    
    # JSON поля для расширяемости
    settings = Column(JSON, default=dict)  # Дополнительные настройки
    analytics = Column(JSON, default=dict)  # Аналитические данные
    
    # Связи
    author = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary="article_tags", back_populates="articles")
    
    # Индексы для производительности
    __table_args__ = (
        Index("idx_article_author_status", "author_id", "status"),
        Index("idx_article_published", "published_at", "status", "visibility"),
        Index("idx_article_views", "views_count"),
    )
    
    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}', status='{self.status}')>"
    
    @property
    def is_published(self) -> bool:
        """Проверка, опубликована ли статья"""
        return self.status == ArticleStatus.PUBLISHED
    
    @property
    def is_public(self) -> bool:
        """Проверка, публична ли статья"""
        return (
            self.status == ArticleStatus.PUBLISHED and 
            self.visibility == ArticleVisibility.PUBLIC
        )
    
    @property
    def public_url(self) -> str:
        """Публичный URL статьи"""
        return f"/{self.author.username}/{self.slug}"
    
    def to_dict(self, include_content: bool = True) -> dict:
        """Преобразование в словарь"""
        data = {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "subtitle": self.subtitle,
            "excerpt": self.excerpt,
            "cover_image": self.cover_image,
            "reading_time": self.reading_time,
            "word_count": self.word_count,
            "status": self.status.value,
            "visibility": self.visibility.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "published_at": self.published_at,
            "views_count": self.views_count,
            "likes_count": self.likes_count,
            "comments_count": self.comments_count,
            "shares_count": self.shares_count,
            "allow_comments": self.allow_comments,
            "is_featured": self.is_featured,
            "is_pinned": self.is_pinned,
            "author": self.author.public_profile if self.author else None,
            "tags": [tag.name for tag in self.tags] if self.tags else [],
            "public_url": self.public_url
        }
        
        if include_content:
            data["content"] = self.content
            
        return data
