import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'
import { UserProfile } from '@/components/profile/UserProfile'
import { Article } from '@/types'

// Mock data - в реальном приложении это будет загружаться с сервера
const mockUser = {
  id: 1,
  email: 'ivan@example.com',
  username: 'ivan_dev',
  full_name: 'Иван Петров',
  avatar_url: '/avatars/ivan.jpg',
  bio: 'Full-stack разработчик с 5-летним опытом. Специализируюсь на React, Node.js и Python. Люблю писать о технологиях и делиться знаниями.',
  is_verified: true,
  created_at: '2023-01-15T10:30:00Z',
  updated_at: '2024-01-15T10:30:00Z',
  followers_count: 89,
  following_count: 45,
  articles_count: 12
}

const mockArticles: Article[] = [
  {
    id: 1,
    title: 'Как создать современный блог на Next.js и FastAPI',
    slug: 'how-to-create-modern-blog-nextjs-fastapi',
    content: 'Полное руководство по созданию блог-платформы...',
    excerpt: 'Полное руководство по созданию полнофункциональной блог-платформы с использованием современных технологий.',
    cover_image: '/images/blog-nextjs-fastapi.jpg',
    is_published: true,
    is_private: false,
    read_time: 8,
    views_count: 1240,
    likes_count: 89,
    comments_count: 23,
    created_at: '2024-01-15T10:30:00Z',
    updated_at: '2024-01-15T10:30:00Z',
    published_at: '2024-01-15T10:30:00Z',
    author: mockUser,
    tags: [
      { id: 1, name: 'Next.js', slug: 'nextjs', articles_count: 15 },
      { id: 2, name: 'FastAPI', slug: 'fastapi', articles_count: 8 },
      { id: 3, name: 'Блог', slug: 'blog', articles_count: 25 }
    ]
  },
  {
    id: 2,
    title: 'TypeScript: от новичка до профессионала',
    slug: 'typescript-from-beginner-to-pro',
    content: 'Подробный разбор возможностей TypeScript...',
    excerpt: 'Подробный разбор возможностей TypeScript, лучших практик и продвинутых техник для создания надежного кода.',
    cover_image: '/images/typescript-guide.jpg',
    is_published: true,
    is_private: false,
    read_time: 12,
    views_count: 890,
    likes_count: 67,
    comments_count: 15,
    created_at: '2024-01-14T14:20:00Z',
    updated_at: '2024-01-14T14:20:00Z',
    published_at: '2024-01-14T14:20:00Z',
    author: mockUser,
    tags: [
      { id: 4, name: 'TypeScript', slug: 'typescript', articles_count: 20 },
      { id: 5, name: 'JavaScript', slug: 'javascript', articles_count: 30 }
    ]
  },
  {
    id: 3,
    title: 'Оптимизация производительности React приложений',
    slug: 'react-performance-optimization',
    content: 'Практические советы и техники для улучшения производительности...',
    excerpt: 'Практические советы и техники для улучшения производительности ваших React приложений.',
    cover_image: '/images/react-performance.jpg',
    is_published: true,
    is_private: false,
    read_time: 10,
    views_count: 1560,
    likes_count: 124,
    comments_count: 31,
    created_at: '2024-01-13T09:15:00Z',
    updated_at: '2024-01-13T09:15:00Z',
    published_at: '2024-01-13T09:15:00Z',
    author: mockUser,
    tags: [
      { id: 6, name: 'React', slug: 'react', articles_count: 18 },
      { id: 7, name: 'Производительность', slug: 'performance', articles_count: 12 }
    ]
  }
]

interface ProfilePageProps {
  params: {
    username: string
  }
}

export default function ProfilePage({ params }: ProfilePageProps) {
  // В реальном приложении здесь будет загрузка данных с сервера
  const isOwnProfile = params.username === 'ivan_dev' // Заглушка
  const isFollowing = false // Заглушка

  return (
    <>
      <Header />
      
      <main className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <UserProfile
            user={mockUser}
            articles={mockArticles}
            isOwnProfile={isOwnProfile}
            isFollowing={isFollowing}
            followersCount={mockUser.followers_count}
            followingCount={mockUser.following_count}
          />
        </div>
      </main>

      <Footer />
    </>
  )
} 