'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'
import { Button } from '@/components/ui/Button'
import { Card, CardContent } from '@/components/ui/Card'
import { 
  MagnifyingGlassIcon,
  FunnelIcon,
  HeartIcon,
  BookmarkIcon,
  EyeIcon,
  UserCircleIcon,
  CalendarIcon
} from '@heroicons/react/24/outline'

interface Article {
  id: number
  title: string
  excerpt: string
  author: {
    username: string
    full_name: string
    avatar_url?: string
  }
  published_at: string
  read_time: number
  views: number
  likes: number
  tags: string[]
  cover_image?: string
}

const mockArticles: Article[] = [
  {
    id: 1,
    title: 'Как создать современный блог на Next.js и FastAPI',
    excerpt: 'Полное руководство по созданию полнофункциональной блог-платформы с использованием современных технологий. Рассмотрим архитектуру, настройку и деплой.',
    author: {
      username: 'ivan_dev',
      full_name: 'Иван Петров',
      avatar_url: '/avatars/ivan.jpg'
    },
    published_at: '2024-01-15T10:30:00Z',
    read_time: 8,
    views: 1240,
    likes: 89,
    tags: ['Next.js', 'FastAPI', 'Блог', 'Разработка']
  },
  {
    id: 2,
    title: 'TypeScript: от новичка до профессионала',
    excerpt: 'Подробный разбор возможностей TypeScript, лучших практик и продвинутых техник для создания надежного кода.',
    author: {
      username: 'maria_ts',
      full_name: 'Мария Сидорова'
    },
    published_at: '2024-01-14T14:20:00Z',
    read_time: 12,
    views: 890,
    likes: 67,
    tags: ['TypeScript', 'JavaScript', 'Программирование']
  },
  {
    id: 3,
    title: 'Оптимизация производительности React приложений',
    excerpt: 'Практические советы и техники для улучшения производительности ваших React приложений. От мемоизации до ленивой загрузки.',
    author: {
      username: 'alex_react',
      full_name: 'Алексей Козлов',
      avatar_url: '/avatars/alex.jpg'
    },
    published_at: '2024-01-13T09:15:00Z',
    read_time: 10,
    views: 1560,
    likes: 124,
    tags: ['React', 'Производительность', 'Оптимизация']
  },
  {
    id: 4,
    title: 'Docker для разработчиков: полное руководство',
    excerpt: 'Изучите Docker с нуля до продвинутого уровня. Контейнеризация приложений, оркестрация и лучшие практики.',
    author: {
      username: 'docker_master',
      full_name: 'Дмитрий Волков'
    },
    published_at: '2024-01-12T16:45:00Z',
    read_time: 15,
    views: 2100,
    likes: 156,
    tags: ['Docker', 'DevOps', 'Контейнеризация']
  }
]

export default function ExplorePage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedTag, setSelectedTag] = useState<string | null>(null)
  const [sortBy, setSortBy] = useState<'latest' | 'popular' | 'trending'>('latest')

  const filteredArticles = mockArticles.filter(article => {
    const matchesSearch = article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         article.excerpt.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         article.author.full_name.toLowerCase().includes(searchQuery.toLowerCase())
    
    const matchesTag = !selectedTag || article.tags.includes(selectedTag)
    
    return matchesSearch && matchesTag
  })

  const allTags = Array.from(new Set(mockArticles.flatMap(article => article.tags)))

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  return (
    <>
      <Header />
      
      <main className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Исследовать статьи
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              Откройте для себя интересные статьи от талантливых авторов
            </p>
          </div>

          {/* Search and Filters */}
          <div className="mb-8 space-y-4">
            {/* Search Bar */}
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Поиск статей, авторов или тегов..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-800 dark:border-gray-600 dark:text-white"
              />
            </div>

            {/* Filters */}
            <div className="flex flex-wrap items-center gap-4">
              <div className="flex items-center space-x-2">
                <FunnelIcon className="h-5 w-5 text-gray-500" />
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Сортировать:</span>
              </div>
              
              <div className="flex space-x-2">
                {[
                  { value: 'latest', label: 'Новые' },
                  { value: 'popular', label: 'Популярные' },
                  { value: 'trending', label: 'В тренде' }
                ].map((option) => (
                  <button
                    key={option.value}
                    onClick={() => setSortBy(option.value as any)}
                    className={`px-3 py-1 text-sm rounded-full transition-colors ${
                      sortBy === option.value
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
                    }`}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Tags */}
            <div className="flex flex-wrap gap-2">
              {allTags.map((tag) => (
                <button
                  key={tag}
                  onClick={() => setSelectedTag(selectedTag === tag ? null : tag)}
                  className={`px-3 py-1 text-sm rounded-full transition-colors ${
                    selectedTag === tag
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
                  }`}
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>

          {/* Articles Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredArticles.map((article) => (
              <Card key={article.id} className="hover:shadow-lg transition-shadow">
                {article.cover_image && (
                  <div className="aspect-video bg-gray-200 dark:bg-gray-700 rounded-t-lg overflow-hidden">
                    <img
                      src={article.cover_image}
                      alt={article.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                )}
                <CardContent className="p-6">
                  <div className="flex items-center space-x-2 mb-3">
                    {article.author.avatar_url ? (
                      <img
                        src={article.author.avatar_url}
                        alt={article.author.full_name}
                        className="w-8 h-8 rounded-full"
                      />
                    ) : (
                      <UserCircleIcon className="w-8 h-8 text-gray-400" />
                    )}
                    <div>
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        {article.author.full_name}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        @{article.author.username}
                      </p>
                    </div>
                  </div>

                  <Link href={`/articles/${article.id}`}>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                      {article.title}
                    </h3>
                  </Link>

                  <p className="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-3">
                    {article.excerpt}
                  </p>

                  <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 mb-4">
                    <div className="flex items-center space-x-4">
                      <span className="flex items-center">
                        <CalendarIcon className="h-4 w-4 mr-1" />
                        {formatDate(article.published_at)}
                      </span>
                      <span>{article.read_time} мин чтения</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                      <span className="flex items-center">
                        <EyeIcon className="h-4 w-4 mr-1" />
                        {article.views}
                      </span>
                      <span className="flex items-center">
                        <HeartIcon className="h-4 w-4 mr-1" />
                        {article.likes}
                      </span>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <Button variant="ghost" size="sm">
                        <HeartIcon className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <BookmarkIcon className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-1 mt-3">
                    {article.tags.slice(0, 3).map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded dark:bg-gray-700 dark:text-gray-300"
                      >
                        {tag}
                      </span>
                    ))}
                    {article.tags.length > 3 && (
                      <span className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded dark:bg-gray-700 dark:text-gray-300">
                        +{article.tags.length - 3}
                      </span>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Load More */}
          {filteredArticles.length > 0 && (
            <div className="mt-8 text-center">
              <Button variant="outline">
                Загрузить еще
              </Button>
            </div>
          )}

          {/* No Results */}
          {filteredArticles.length === 0 && (
            <div className="text-center py-12">
              <div className="text-gray-400 dark:text-gray-500 mb-4">
                <MagnifyingGlassIcon className="h-16 w-16 mx-auto" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                Статьи не найдены
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Попробуйте изменить поисковый запрос или фильтры
              </p>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </>
  )
} 