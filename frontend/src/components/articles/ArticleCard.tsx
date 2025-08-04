'use client'

import Link from 'next/link'
import { Article } from '@/types'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { 
  HeartIcon, 
  BookmarkIcon, 
  EyeIcon, 
  UserCircleIcon,
  CalendarIcon,
  ClockIcon
} from '@heroicons/react/24/outline'
import { formatDate, formatCompactNumber } from '@/lib/utils'

interface ArticleCardProps {
  article: Article
  showAuthor?: boolean
  showStats?: boolean
  variant?: 'default' | 'compact' | 'featured'
}

export function ArticleCard({ 
  article, 
  showAuthor = true, 
  showStats = true,
  variant = 'default' 
}: ArticleCardProps) {
  const isCompact = variant === 'compact'
  const isFeatured = variant === 'featured'

  return (
    <Card className={`group hover:shadow-lg transition-all duration-200 ${
      isFeatured ? 'ring-2 ring-primary-200 dark:ring-primary-800' : ''
    }`}>
      {article.cover_image && !isCompact && (
        <div className="aspect-video bg-gray-200 dark:bg-gray-700 rounded-t-lg overflow-hidden">
          <img
            src={article.cover_image}
            alt={article.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        </div>
      )}
      
      <CardContent className={`p-6 ${isCompact ? 'p-4' : ''}`}>
        {/* Author info */}
        {showAuthor && (
          <div className="flex items-center space-x-2 mb-3">
            {article.author.avatar_url ? (
              <img
                src={article.author.avatar_url}
                alt={article.author.full_name || article.author.username}
                className="w-8 h-8 rounded-full"
              />
            ) : (
              <UserCircleIcon className="w-8 h-8 text-gray-400" />
            )}
            <div>
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                {article.author.full_name || article.author.username}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                @{article.author.username}
              </p>
            </div>
          </div>
        )}

        {/* Article title */}
        <Link href={`/articles/${article.slug}`}>
          <h3 className={`font-semibold text-gray-900 dark:text-white mb-2 hover:text-primary-600 dark:hover:text-primary-400 transition-colors ${
            isCompact ? 'text-base' : 'text-lg'
          } ${isFeatured ? 'text-xl' : ''}`}>
            {article.title}
          </h3>
        </Link>

        {/* Article excerpt */}
        {!isCompact && (
          <p className="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-2">
            {article.excerpt}
          </p>
        )}

        {/* Meta information */}
        <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 mb-4">
          <div className="flex items-center space-x-4">
            <span className="flex items-center">
              <CalendarIcon className="h-4 w-4 mr-1" />
              {formatDate(article.published_at || article.created_at)}
            </span>
            <span className="flex items-center">
              <ClockIcon className="h-4 w-4 mr-1" />
              {article.read_time} мин
            </span>
          </div>
        </div>

        {/* Stats and actions */}
        {showStats && (
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
              <span className="flex items-center">
                <EyeIcon className="h-4 w-4 mr-1" />
                {formatCompactNumber(article.views_count)}
              </span>
              <span className="flex items-center">
                <HeartIcon className="h-4 w-4 mr-1" />
                {formatCompactNumber(article.likes_count)}
              </span>
            </div>
            
            <div className="flex items-center space-x-2">
              <Button variant="ghost" size="sm" className="p-2">
                <HeartIcon className="h-4 w-4" />
              </Button>
              <Button variant="ghost" size="sm" className="p-2">
                <BookmarkIcon className="h-4 w-4" />
              </Button>
            </div>
          </div>
        )}

        {/* Tags */}
        {article.tags.length > 0 && !isCompact && (
          <div className="flex flex-wrap gap-1 mt-3">
            {article.tags.slice(0, 3).map((tag) => (
              <Link 
                key={tag.id} 
                href={`/tags/${tag.slug}`}
                className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600 transition-colors"
              >
                {tag.name}
              </Link>
            ))}
            {article.tags.length > 3 && (
              <span className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded dark:bg-gray-700 dark:text-gray-300">
                +{article.tags.length - 3}
              </span>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
} 