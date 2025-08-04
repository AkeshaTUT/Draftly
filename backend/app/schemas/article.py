from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import uuid

from app.models.article import ArticleStatus, ArticleVisibility


class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    excerpt: Optional[str] = Field(None, max_length=500)
    cover_image_url: Optional[str] = Field(None, max_length=500)
    cover_image_alt: Optional[str] = Field(None, max_length=255)
    tags: List[str] = Field(default_factory=list)
    allow_comments: bool = True
    allow_likes: bool = True
    visibility: ArticleVisibility = ArticleVisibility.PUBLIC
    
    @field_validator('tags', mode='before')
    @classmethod
    def validate_tags(cls, v):
        if len(v) > 10:
            raise ValueError('Maximum 10 tags allowed')
        for tag in v:
            if len(tag) > 50:
                raise ValueError('Tag length must be less than 50 characters')
            if not tag.replace('-', '').replace('_', '').isalnum():
                raise ValueError('Tags can only contain letters, numbers, hyphens and underscores')
        return list(set(v))  # Remove duplicates
    
    @field_validator('content', mode='before')
    @classmethod
    def validate_content(cls, v):
        if len(v) < 10:
            raise ValueError('Content must be at least 10 characters long')
        if len(v) > 50000:
            raise ValueError('Content must be less than 50,000 characters')
        return v


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=10, max_length=50000)
    excerpt: Optional[str] = Field(None, max_length=500)
    cover_image_url: Optional[str] = Field(None, max_length=500)
    cover_image_alt: Optional[str] = Field(None, max_length=255)
    tags: Optional[List[str]] = None
    status: Optional[ArticleStatus] = None
    visibility: Optional[ArticleVisibility] = None
    allow_comments: Optional[bool] = None
    allow_likes: Optional[bool] = None
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    meta_keywords: Optional[List[str]] = None
    
    @field_validator('tags', mode='before')
    @classmethod
    def validate_tags(cls, v):
        if v is None:
            return v
        if len(v) > 10:
            raise ValueError('Maximum 10 tags allowed')
        for tag in v:
            if len(tag) > 50:
                raise ValueError('Tag length must be less than 50 characters')
            if not tag.replace('-', '').replace('_', '').isalnum():
                raise ValueError('Tags can only contain letters, numbers, hyphens and underscores')
        return list(set(v))
    
    @field_validator('meta_keywords', mode='before')
    @classmethod
    def validate_meta_keywords(cls, v):
        if v is None:
            return v
        if len(v) > 20:
            raise ValueError('Maximum 20 meta keywords allowed')
        return v


class ArticleResponse(ArticleBase):
    id: uuid.UUID
    slug: str
    author_id: uuid.UUID
    status: ArticleStatus
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[List[str]] = None
    is_featured: bool
    is_pinned: bool
    view_count: int
    like_count: int
    comment_count: int
    bookmark_count: int
    rating: float
    rating_count: int
    reading_time: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }


class ArticleDetail(ArticleResponse):
    """Детальная информация о статье с автором"""
    author: dict  # Будет заменено на UserResponse
    is_liked: bool = False
    is_bookmarked: bool = False
    is_following_author: bool = False


class ArticleList(BaseModel):
    """Список статей для пагинации"""
    articles: List[ArticleResponse]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool


class ArticleSearch(BaseModel):
    """Параметры поиска статей"""
    query: Optional[str] = None
    tags: Optional[List[str]] = None
    author_id: Optional[uuid.UUID] = None
    status: Optional[ArticleStatus] = None
    visibility: Optional[ArticleVisibility] = None
    sort_by: str = Field("created_at", pattern="^(created_at|updated_at|published_at|view_count|like_count|rating)$")
    sort_order: str = Field("desc", pattern="^(asc|desc)$")
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


class ArticleStats(BaseModel):
    """Статистика статьи"""
    article_id: uuid.UUID
    view_count: int
    like_count: int
    comment_count: int
    bookmark_count: int
    rating: float
    rating_count: int
    shares_count: int
    unique_visitors: int
    avg_time_on_page: Optional[float] = None  # в секундах


class ArticleView(BaseModel):
    """Просмотр статьи"""
    article_id: uuid.UUID
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None


class ArticleShare(BaseModel):
    """Поделиться статьей"""
    article_id: uuid.UUID
    platform: str = Field(..., pattern="^(twitter|facebook|telegram|linkedin|vk|ok)$")


class ArticleDraft(BaseModel):
    """Черновик статьи"""
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = Field(None, max_length=50000)
    excerpt: Optional[str] = Field(None, max_length=500)
    tags: List[str] = Field(default_factory=list)
    auto_save: bool = True


class ArticlePublish(BaseModel):
    """Публикация статьи"""
    status: ArticleStatus = ArticleStatus.PUBLISHED
    visibility: ArticleVisibility = ArticleVisibility.PUBLIC
    publish_now: bool = True
    scheduled_at: Optional[datetime] = None
    
    @field_validator('scheduled_at', mode='before')
    @classmethod
    def validate_scheduled_at(cls, v):
        if v and v <= datetime.utcnow():
            raise ValueError('Scheduled time must be in the future')
        return v 