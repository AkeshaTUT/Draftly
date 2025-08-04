'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth/AuthProvider'
import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'
import { Button } from '@/components/ui/Button'
import { Card, CardContent, CardHeader } from '@/components/ui/Card'
import Link from 'next/link'
import { 
  PencilSquareIcon,
  DocumentTextIcon,
  EyeIcon,
  HeartIcon,
  BookmarkIcon,
  UserGroupIcon,
  ChartBarIcon,
  PlusIcon
} from '@heroicons/react/24/outline'

export default function DashboardPage() {
  const { user, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/auth/login')
    }
  }, [user, isLoading, router])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <>
      <Header />
      
      <main className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Панель управления
            </h1>
            <p className="mt-2 text-gray-600 dark:text-gray-300">
              Добро пожаловать, {user.full_name || user.username}!
            </p>
          </div>

          {/* Quick Actions */}
          <div className="mb-8">
            <div className="flex flex-wrap gap-4">
              <Link href="/dashboard/write">
                <Button className="flex items-center">
                  <PlusIcon className="mr-2 h-5 w-5" />
                  Написать статью
                </Button>
              </Link>
              <Link href="/dashboard/drafts">
                <Button variant="outline" className="flex items-center">
                  <DocumentTextIcon className="mr-2 h-5 w-5" />
                  Черновики
                </Button>
              </Link>
              <Link href="/dashboard/analytics">
                <Button variant="outline" className="flex items-center">
                  <ChartBarIcon className="mr-2 h-5 w-5" />
                  Аналитика
                </Button>
              </Link>
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <DocumentTextIcon className="h-8 w-8 text-primary-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                      Всего статей
                    </p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">
                      12
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <EyeIcon className="h-8 w-8 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                      Просмотры
                    </p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">
                      2.4K
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <HeartIcon className="h-8 w-8 text-red-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                      Лайки
                    </p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">
                      156
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <UserGroupIcon className="h-8 w-8 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                      Подписчики
                    </p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">
                      89
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Recent Articles */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <Card>
              <CardHeader>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Последние статьи
                </h3>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    {
                      id: 1,
                      title: 'Как создать современный блог на Next.js',
                      status: 'published',
                      views: 450,
                      likes: 23,
                      date: '2024-01-15'
                    },
                    {
                      id: 2,
                      title: 'Руководство по TypeScript для начинающих',
                      status: 'draft',
                      views: 0,
                      likes: 0,
                      date: '2024-01-14'
                    },
                    {
                      id: 3,
                      title: 'Оптимизация производительности React приложений',
                      status: 'published',
                      views: 320,
                      likes: 18,
                      date: '2024-01-12'
                    }
                  ].map((article) => (
                    <div key={article.id} className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                      <div className="flex-1">
                        <h4 className="font-medium text-gray-900 dark:text-white">
                          {article.title}
                        </h4>
                        <div className="flex items-center mt-1 space-x-4 text-sm text-gray-500 dark:text-gray-400">
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            article.status === 'published' 
                              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                              : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                          }`}>
                            {article.status === 'published' ? 'Опубликовано' : 'Черновик'}
                          </span>
                          <span>{article.views} просмотров</span>
                          <span>{article.likes} лайков</span>
                        </div>
                      </div>
                      <Link href={`/dashboard/articles/${article.id}/edit`}>
                        <Button variant="ghost" size="sm">
                          <PencilSquareIcon className="h-4 w-4" />
                        </Button>
                      </Link>
                    </div>
                  ))}
                </div>
                <div className="mt-4">
                  <Link href="/dashboard/articles">
                    <Button variant="outline" className="w-full">
                      Посмотреть все статьи
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>

            {/* Recent Activity */}
            <Card>
              <CardHeader>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Последняя активность
                </h3>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    {
                      id: 1,
                      type: 'comment',
                      message: 'Новый комментарий к статье "Как создать современный блог"',
                      time: '2 часа назад'
                    },
                    {
                      id: 2,
                      type: 'like',
                      message: 'Ваша статья получила 5 новых лайков',
                      time: '4 часа назад'
                    },
                    {
                      id: 3,
                      type: 'follow',
                      message: 'Новый подписчик: @alex_dev',
                      time: '1 день назад'
                    },
                    {
                      id: 4,
                      type: 'publish',
                      message: 'Статья "Руководство по TypeScript" опубликована',
                      time: '2 дня назад'
                    }
                  ].map((activity) => (
                    <div key={activity.id} className="flex items-start space-x-3 p-3 border border-gray-200 dark:border-gray-700 rounded-lg">
                      <div className="flex-shrink-0 w-2 h-2 bg-primary-600 rounded-full mt-2"></div>
                      <div className="flex-1">
                        <p className="text-sm text-gray-900 dark:text-white">
                          {activity.message}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                          {activity.time}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-4">
                  <Link href="/dashboard/notifications">
                    <Button variant="outline" className="w-full">
                      Посмотреть все уведомления
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      <Footer />
    </>
  )
} 