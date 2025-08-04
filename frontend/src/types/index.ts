// User types
export interface User {
  id: number
  email: string
  username: string
  full_name?: string
  avatar_url?: string
  bio?: string
  is_verified: boolean
  created_at: string
  updated_at: string
  followers_count?: number
  following_count?: number
  articles_count?: number
}

// Article types
export interface Article {
  id: number
  title: string
  slug: string
  content: string
  excerpt: string
  cover_image?: string
  is_published: boolean
  is_private: boolean
  read_time: number
  views_count: number
  likes_count: number
  comments_count: number
  created_at: string
  updated_at: string
  published_at?: string
  author: User
  tags: Tag[]
  category?: Category
}

// Tag types
export interface Tag {
  id: number
  name: string
  slug: string
  description?: string
  articles_count?: number
}

// Category types
export interface Category {
  id: number
  name: string
  slug: string
  description?: string
  color?: string
  articles_count?: number
}

// Comment types
export interface Comment {
  id: number
  content: string
  created_at: string
  updated_at: string
  author: User
  article_id: number
  parent_id?: number
  replies?: Comment[]
  likes_count: number
  is_edited: boolean
}

// Notification types
export interface Notification {
  id: number
  type: 'like' | 'comment' | 'follow' | 'mention' | 'system'
  title: string
  message: string
  is_read: boolean
  created_at: string
  data?: Record<string, any>
  sender?: User
  article?: Article
}

// Auth types
export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  username: string
  password: string
  full_name?: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  user: User
  expires_in: number
}

// API Response types
export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  per_page: number
  pages: number
  has_next: boolean
  has_prev: boolean
}

// Search types
export interface SearchFilters {
  query?: string
  tags?: string[]
  category?: string
  author?: string
  sort_by?: 'latest' | 'popular' | 'trending' | 'oldest'
  date_from?: string
  date_to?: string
}

// File upload types
export interface FileUpload {
  id: string
  filename: string
  original_name: string
  mime_type: string
  size: number
  url: string
  created_at: string
}

// Dashboard types
export interface DashboardStats {
  total_articles: number
  total_views: number
  total_likes: number
  total_comments: number
  total_followers: number
  total_following: number
  recent_articles: Article[]
  recent_activity: Activity[]
}

export interface Activity {
  id: number
  type: 'article_published' | 'article_liked' | 'comment_received' | 'new_follower' | 'mention'
  message: string
  created_at: string
  data?: Record<string, any>
}

// Payment types
export interface Payment {
  id: number
  amount: number
  currency: string
  status: 'pending' | 'completed' | 'failed' | 'cancelled'
  payment_method: string
  created_at: string
  description?: string
}

// Settings types
export interface UserSettings {
  email_notifications: boolean
  push_notifications: boolean
  telegram_notifications: boolean
  privacy_level: 'public' | 'private' | 'friends'
  allow_comments: boolean
  allow_likes: boolean
  theme: 'light' | 'dark' | 'system'
  language: string
}

// Form types
export interface ArticleFormData {
  title: string
  content: string
  excerpt?: string
  cover_image?: File
  tags: string[]
  category_id?: number
  is_published: boolean
  is_private: boolean
}

export interface ProfileFormData {
  full_name: string
  bio?: string
  avatar?: File
  website?: string
  location?: string
  social_links?: {
    twitter?: string
    github?: string
    linkedin?: string
  }
}

// Error types
export interface ApiError {
  detail: string
  code?: string
  field?: string
}

// UI types
export interface Toast {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
}

export interface Modal {
  id: string
  isOpen: boolean
  title?: string
  content?: React.ReactNode
}

// Navigation types
export interface NavItem {
  label: string
  href: string
  icon?: React.ComponentType<{ className?: string }>
  children?: NavItem[]
  external?: boolean
}

// Theme types
export type Theme = 'light' | 'dark' | 'system'

// Localization types
export interface Locale {
  code: string
  name: string
  flag?: string
}

// SEO types
export interface SEOData {
  title: string
  description: string
  keywords?: string[]
  image?: string
  url?: string
  type?: 'website' | 'article' | 'profile'
  author?: string
  published_time?: string
  modified_time?: string
}

// WebSocket types
export interface WebSocketMessage {
  type: string
  data: any
  timestamp: string
}

// Analytics types
export interface AnalyticsData {
  page_views: number
  unique_visitors: number
  bounce_rate: number
  avg_session_duration: number
  top_pages: Array<{
    path: string
    views: number
  }>
  top_sources: Array<{
    source: string
    views: number
  }>
}

// Export all types
export type {
  User,
  Article,
  Tag,
  Category,
  Comment,
  Notification,
  LoginCredentials,
  RegisterData,
  AuthResponse,
  ApiResponse,
  PaginatedResponse,
  SearchFilters,
  FileUpload,
  DashboardStats,
  Activity,
  Payment,
  UserSettings,
  ArticleFormData,
  ProfileFormData,
  ApiError,
  Toast,
  Modal,
  NavItem,
  Theme,
  Locale,
  SEOData,
  WebSocketMessage,
  AnalyticsData
} 