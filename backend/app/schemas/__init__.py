# Импорт всех схем
from app.schemas.user import (
    UserBase, UserCreate, UserUpdate, UserResponse, UserProfile, UserList,
    UserLogin, UserOAuth, PasswordChange, PasswordReset, PasswordResetConfirm,
    TelegramConnect, UserPreferences
)
from app.schemas.article import (
    ArticleBase, ArticleCreate, ArticleUpdate, ArticleResponse, ArticleDetail,
    ArticleList, ArticleSearch, ArticleStats, ArticleView, ArticleShare,
    ArticleDraft, ArticlePublish
)

# Экспорт всех схем
__all__ = [
    # User schemas
    "UserBase", "UserCreate", "UserUpdate", "UserResponse", "UserProfile", "UserList",
    "UserLogin", "UserOAuth", "PasswordChange", "PasswordReset", "PasswordResetConfirm",
    "TelegramConnect", "UserPreferences",
    
    # Article schemas
    "ArticleBase", "ArticleCreate", "ArticleUpdate", "ArticleResponse", "ArticleDetail",
    "ArticleList", "ArticleSearch", "ArticleStats", "ArticleView", "ArticleShare",
    "ArticleDraft", "ArticlePublish",
] 