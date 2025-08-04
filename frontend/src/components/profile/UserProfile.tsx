'use client'

import { useState } from 'react'
import Link from 'next/link'
import { User, Article } from '@/types'
import { Card, CardContent, CardHeader } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { ArticleList } from '@/components/articles/ArticleList'
import { 
  UserCircleIcon,
  CalendarIcon,
  MapPinIcon,
  LinkIcon,
  HeartIcon,
  BookmarkIcon,
  EyeIcon,
  UserGroupIcon,
  PencilSquareIcon
} from '@heroicons/react/24/outline'
import { formatDate, formatCompactNumber } from '@/lib/utils'

interface UserProfileProps {
  user: User
  articles: Article[]
  isOwnProfile?: boolean
  isFollowing?: boolean
  followersCount?: number
  followingCount?: number
}

export function UserProfile({
  user,
  articles,
  isOwnProfile = false,
  isFollowing = false,
  followersCount = 0,
  followingCount = 0
}: UserProfileProps) {
  const [activeTab, setActiveTab] = useState<'articles' | 'likes' | 'bookmarks'>('articles')

  const tabs = [
    { id: 'articles', label: 'Статьи', count: articles.length },
    { id: 'likes', label: 'Лайки', count: 0 },
    { id: 'bookmarks', label: 'Закладки', count: 0 }
  ]

  return (
    <div className="space-y-6">
      {/* Profile Header */}
      <Card>
        <CardContent className="p-6">
          <div className="flex flex-col md:flex-row items-start md:items-center space-y-4 md:space-y-0 md:space-x-6">
            {/* Avatar */}
            <div className="flex-shrink-0">
              {user.avatar_url ? (
                <img
                  src={user.avatar_url}
                  alt={user.full_name || user.username}
                  className="w-24 h-24 rounded-full object-cover"
                />
              ) : (
                <div className="w-24 h-24 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
                  <UserCircleIcon className="w-16 h-16 text-gray-400" />
                </div>
              )}
            </div>

            {/* Profile Info */}
            <div className="flex-1 min-w-0">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                    {user.full_name || user.username}
                  </h1>
                  <p className="text-gray-500 dark:text-gray-400">
                    @{user.username}
                  </p>
                  {user.bio && (
                    <p className="mt-2 text-gray-600 dark:text-gray-300">
                      {user.bio}
                    </p>
                  )}
                </div>

                {/* Action Buttons */}
                <div className="mt-4 sm:mt-0 flex space-x-2">
                  {isOwnProfile ? (
                    <Link href="/profile/edit">
                      <Button variant="outline" className="flex items-center">
                        <PencilSquareIcon className="h-4 w-4 mr-2" />
                        Редактировать
                      </Button>
                    </Link>
                  ) : (
                    <Button 
                      variant={isFollowing ? 'outline' : 'primary'}
                      className="flex items-center"
                    >
                      <UserGroupIcon className="h-4 w-4 mr-2" />
                      {isFollowing ? 'Отписаться' : 'Подписаться'}
                    </Button>
                  )}
                </div>
              </div>

              {/* Stats */}
              <div className="mt-4 flex items-center space-x-6 text-sm text-gray-500 dark:text-gray-400">
                <div className="flex items-center">
                  <CalendarIcon className="h-4 w-4 mr-1" />
                  На сайте с {formatDate(user.created_at, { year: 'numeric', month: 'long' })}
                </div>
                {user.is_verified && (
                  <span className="flex items-center text-primary-600 dark:text-primary-400">
                    ✓ Проверенный автор
                  </span>
                )}
              </div>

              {/* Follow Stats */}
              <div className="mt-4 flex items-center space-x-6">
                <Link href={`/users/${user.username}/followers`} className="hover:text-primary-600 dark:hover:text-primary-400">
                  <span className="font-semibold text-gray-900 dark:text-white">
                    {formatCompactNumber(followersCount)}
                  </span>
                  <span className="text-gray-500 dark:text-gray-400 ml-1">
                    подписчиков
                  </span>
                </Link>
                <Link href={`/users/${user.username}/following`} className="hover:text-primary-600 dark:hover:text-primary-400">
                  <span className="font-semibold text-gray-900 dark:text-white">
                    {formatCompactNumber(followingCount)}
                  </span>
                  <span className="text-gray-500 dark:text-gray-400 ml-1">
                    подписок
                  </span>
                </Link>
                <div>
                  <span className="font-semibold text-gray-900 dark:text-white">
                    {formatCompactNumber(articles.length)}
                  </span>
                  <span className="text-gray-500 dark:text-gray-400 ml-1">
                    статей
                  </span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Card>
        <CardHeader className="pb-0">
          <div className="border-b border-gray-200 dark:border-gray-700">
            <nav className="-mb-px flex space-x-8">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                  }`}
                >
                  {tab.label}
                  {tab.count > 0 && (
                    <span className="ml-2 bg-gray-100 text-gray-900 py-0.5 px-2.5 rounded-full text-xs dark:bg-gray-700 dark:text-gray-300">
                      {tab.count}
                    </span>
                  )}
                </button>
              ))}
            </nav>
          </div>
        </CardHeader>

        <CardContent className="pt-6">
          {/* Tab Content */}
          {activeTab === 'articles' && (
            <ArticleList
              articles={articles}
              variant="grid"
              showFilters={articles.length > 0}
              emptyMessage="У этого автора пока нет статей"
            />
          )}

          {activeTab === 'likes' && (
            <div className="text-center py-12">
              <HeartIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                Понравившиеся статьи
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Здесь будут отображаться статьи, которые понравились автору
              </p>
            </div>
          )}

          {activeTab === 'bookmarks' && (
            <div className="text-center py-12">
              <BookmarkIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                Закладки
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Здесь будут отображаться сохраненные статьи
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
} 