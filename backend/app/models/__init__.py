# Импорт всех моделей для Alembic
from app.models.user import User, UserRole, UserStatus
from app.models.article import Article, ArticleStatus, ArticleVisibility
from app.models.tag import Tag
from app.models.interaction import Comment, CommentStatus, Like, Bookmark, Notification, NotificationType
from app.models.payment import Payment, PaymentStatus

# Экспорт всех моделей
__all__ = [
    # User models
    "User", "UserRole", "UserStatus",
    
    # Article models
    "Article", "ArticleStatus", "ArticleVisibility",
    
    # Tag models
    "Tag",
    
    # Interaction models
    "Comment", "CommentStatus", "Like", "Bookmark", "Notification", "NotificationType",
    
    # Payment models
    "Payment", "PaymentStatus",
] 