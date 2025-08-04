'use client'

import { useState } from 'react'
import { Article } from '@/types'
import { ArticleCard } from './ArticleCard'
import { Button } from '@/components/ui/Button'
import { Card, CardContent } from '@/components/ui/Card'
import { 
  MagnifyingGlassIcon,
  FunnelIcon,
  ChevronLeftIcon,
  ChevronRightIcon
} from '@heroicons/react/24/outline'

interface ArticleListProps {
  articles: Article[]
  title?: string
  showFilters?: boolean
  showPagination?: boolean
  itemsPerPage?: number
  variant?: 'grid' | 'list'
  emptyMessage?: string
}

export function ArticleList({
  articles,
  title,
  showFilters = false,
  showPagination = false,
  itemsPerPage = 12,
  variant = 'grid',
  emptyMessage = 'Статьи не найдены'
}: ArticleListProps) {
  const [currentPage, setCurrentPage] = useState(1)
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState<'latest' | 'popular' | 'trending'>('latest')

  // Filter articles based on search query
  const filteredArticles = articles.filter(article =>
    article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    article.excerpt.toLowerCase().includes(searchQuery.toLowerCase()) ||
    article.author.full_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    article.author.username.toLowerCase().includes(searchQuery.toLowerCase())
  )

  // Sort articles
  const sortedArticles = [...filteredArticles].sort((a, b) => {
    switch (sortBy) {
      case 'popular':
        return b.likes_count - a.likes_count
      case 'trending':
        return b.views_count - a.views_count
      case 'latest':
      default:
        return new Date(b.published_at || b.created_at).getTime() - 
               new Date(a.published_at || a.created_at).getTime()
    }
  })

  // Pagination
  const totalPages = Math.ceil(sortedArticles.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const currentArticles = sortedArticles.slice(startIndex, endIndex)

  const handlePageChange = (page: number) => {
    setCurrentPage(page)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  if (articles.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-400 dark:text-gray-500 mb-4">
          <MagnifyingGlassIcon className="h-16 w-16 mx-auto" />
        </div>
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
          {emptyMessage}
        </h3>
        <p className="text-gray-600 dark:text-gray-300">
          Попробуйте изменить поисковый запрос или фильтры
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      {title && (
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            {title}
          </h2>
          {showFilters && (
            <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
              <span>{filteredArticles.length} статей</span>
            </div>
          )}
        </div>
      )}

      {/* Filters */}
      {showFilters && (
        <Card>
          <CardContent className="p-4">
            <div className="flex flex-col sm:flex-row gap-4">
              {/* Search */}
              <div className="flex-1">
                <div className="relative">
                  <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Поиск статей..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-800 dark:border-gray-600 dark:text-white"
                  />
                </div>
              </div>

              {/* Sort */}
              <div className="flex items-center space-x-2">
                <FunnelIcon className="h-5 w-5 text-gray-500" />
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as any)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-800 dark:border-gray-600 dark:text-white"
                >
                  <option value="latest">Новые</option>
                  <option value="popular">Популярные</option>
                  <option value="trending">В тренде</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Articles Grid/List */}
      <div className={
        variant === 'grid' 
          ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
          : 'space-y-4'
      }>
        {currentArticles.map((article) => (
          <ArticleCard
            key={article.id}
            article={article}
            variant={variant === 'list' ? 'compact' : 'default'}
          />
        ))}
      </div>

      {/* Pagination */}
      {showPagination && totalPages > 1 && (
        <div className="flex items-center justify-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage === 1}
          >
            <ChevronLeftIcon className="h-4 w-4" />
            Назад
          </Button>

          <div className="flex items-center space-x-1">
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
              <Button
                key={page}
                variant={currentPage === page ? 'primary' : 'outline'}
                size="sm"
                onClick={() => handlePageChange(page)}
                className="w-10 h-10"
              >
                {page}
              </Button>
            ))}
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            Вперед
            <ChevronRightIcon className="h-4 w-4" />
          </Button>
        </div>
      )}

      {/* Results info */}
      {showFilters && (
        <div className="text-center text-sm text-gray-500 dark:text-gray-400">
          Показано {currentArticles.length} из {filteredArticles.length} статей
          {searchQuery && ` по запросу "${searchQuery}"`}
        </div>
      )}
    </div>
  )
} 