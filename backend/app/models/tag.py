"""
Модель тега
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

# Таблица связи многие-ко-многим для статей и тегов
article_tags = Table(
    "article_tags",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now())
)

class Tag(Base):
    """Модель тега"""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Основная информация
    name = Column(String(50), unique=True, index=True, nullable=False)
    slug = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Статистика
    articles_count = Column(Integer, default=0)
    
    # Связи
    articles = relationship("Article", secondary=article_tags, back_populates="tags")
    
    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}', slug='{self.slug}')>"
    
    def to_dict(self) -> dict:
        """Преобразование в словарь"""
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "articles_count": self.articles_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
