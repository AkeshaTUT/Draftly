import Link from 'next/link'
import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'
import { Button } from '@/components/ui/Button'
import { Card, CardContent } from '@/components/ui/Card'
import { 
  ArrowRightIcon, 
  PencilSquareIcon, 
  UserGroupIcon, 
  BookmarkIcon,
  SparklesIcon,
  ShieldCheckIcon,
  RocketLaunchIcon
} from '@heroicons/react/24/outline'

export default function HomePage() {
  return (
    <>
      <Header />
      
      <main>
        {/* Hero Section */}
        <section className="relative overflow-hidden bg-white py-16 dark:bg-gray-950 sm:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-4xl text-center">
              <div className="mb-8">
                <span className="inline-flex items-center rounded-full bg-primary-50 px-3 py-1 text-sm font-medium text-primary-700 dark:bg-primary-900/20 dark:text-primary-300">
                  <SparklesIcon className="mr-1 h-4 w-4" />
                  Новая платформа для авторов
                </span>
              </div>
              
              <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl">
                Современная{' '}
                <span className="bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
                  блог-платформа
                </span>
              </h1>
              
              <p className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300">
                Создавайте, публикуйте и делитесь своими идеями с миром. 
                Профессиональный аналог Teletype.in с расширенными возможностями 
                для современных авторов.
              </p>
              
              <div className="mt-10 flex items-center justify-center gap-x-6">
                <Link href="/auth/signup">
                  <Button size="lg" className="group">
                    Начать писать
                    <ArrowRightIcon className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                  </Button>
                </Link>
                
                <Link href="/explore">
                  <Button variant="outline" size="lg">
                    Читать статьи
                  </Button>
                </Link>
              </div>
            </div>
          </div>
          
          {/* Background decoration */}
          <div className="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)]">
            <div className="relative left-[calc(50%+3rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 bg-gradient-to-tr from-primary-600 to-purple-600 opacity-20 sm:left-[calc(50%+36rem)] sm:w-[72.1875rem]" />
          </div>
        </section>

        {/* Features Section */}
        <section className="py-16 sm:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
                Всё что нужно автору
              </h2>
              <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
                Мощные инструменты для создания и продвижения контента
              </p>
            </div>
            
            <div className="mx-auto mt-16 max-w-5xl">
              <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
                <Card className="p-6 hover:shadow-lg transition-shadow">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100 dark:bg-primary-900/20">
                    <PencilSquareIcon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                  </div>
                  <h3 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
                    Markdown редактор
                  </h3>
                  <p className="mt-2 text-gray-600 dark:text-gray-300">
                    Продвинутый редактор с поддержкой Markdown, превью в реальном времени и автосохранением.
                  </p>
                </Card>
                
                <Card className="p-6 hover:shadow-lg transition-shadow">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100 dark:bg-primary-900/20">
                    <UserGroupIcon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                  </div>
                  <h3 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
                    Сообщество
                  </h3>
                  <p className="mt-2 text-gray-600 dark:text-gray-300">
                    Подписки на авторов, комментарии с реакциями и система уведомлений.
                  </p>
                </Card>
                
                <Card className="p-6 hover:shadow-lg transition-shadow">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100 dark:bg-primary-900/20">
                    <BookmarkIcon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                  </div>
                  <h3 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
                    Организация
                  </h3>
                  <p className="mt-2 text-gray-600 dark:text-gray-300">
                    Теги, категории, черновики и мощный поиск по содержимому.
                  </p>
                </Card>

                <Card className="p-6 hover:shadow-lg transition-shadow">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100 dark:bg-primary-900/20">
                    <ShieldCheckIcon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                  </div>
                  <h3 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
                    Безопасность
                  </h3>
                  <p className="mt-2 text-gray-600 dark:text-gray-300">
                    Защита от XSS/CSRF, rate limiting и контент-фильтрация.
                  </p>
                </Card>

                <Card className="p-6 hover:shadow-lg transition-shadow">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100 dark:bg-primary-900/20">
                    <RocketLaunchIcon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                  </div>
                  <h3 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
                    Производительность
                  </h3>
                  <p className="mt-2 text-gray-600 dark:text-gray-300">
                    Быстрая загрузка, оптимизация SEO и PWA поддержка.
                  </p>
                </Card>

                <Card className="p-6 hover:shadow-lg transition-shadow">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-100 dark:bg-primary-900/20">
                    <SparklesIcon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                  </div>
                  <h3 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
                    Монетизация
                  </h3>
                  <p className="mt-2 text-gray-600 dark:text-gray-300">
                    Донаты, премиум контент и партнерская программа.
                  </p>
                </Card>
              </div>
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="bg-primary-50 py-16 dark:bg-primary-950/10 sm:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-4xl">
              <div className="grid grid-cols-1 gap-8 sm:grid-cols-3">
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary-600 dark:text-primary-400">
                    1000+
                  </div>
                  <div className="mt-2 text-sm text-gray-600 dark:text-gray-300">
                    Авторов
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary-600 dark:text-primary-400">
                    5000+
                  </div>
                  <div className="mt-2 text-sm text-gray-600 dark:text-gray-300">
                    Статей
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary-600 dark:text-primary-400">
                    50K+
                  </div>
                  <div className="mt-2 text-sm text-gray-600 dark:text-gray-300">
                    Читателей
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 sm:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white">
                Готовы начать?
              </h2>
              <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
                Присоединяйтесь к сообществу авторов и читателей уже сегодня
              </p>
              <div className="mt-8">
                <Link href="/auth/signup">
                  <Button size="lg">
                    Создать аккаунт бесплатно
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </>
  )
}
