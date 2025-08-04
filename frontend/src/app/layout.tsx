import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import '../styles/globals.css'
import { Providers } from './providers'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ subsets: ['latin', 'cyrillic'] })

export const metadata: Metadata = {
  title: {
    default: 'Teletype.in Analog - Современная блог-платформа',
    template: '%s | Teletype.in Analog'
  },
  description: 'Создавайте, публикуйте и делитесь своими идеями с миром. Профессиональный аналог Teletype.in с расширенными возможностями.',
  keywords: ['блог', 'платформа', 'писательство', 'контент', 'markdown', 'сообщество'],
  authors: [{ name: 'Teletype.in Analog Team' }],
  creator: 'Teletype.in Analog',
  publisher: 'Teletype.in Analog',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    type: 'website',
    locale: 'ru_RU',
    url: '/',
    title: 'Teletype.in Analog - Современная блог-платформа',
    description: 'Создавайте, публикуйте и делитесь своими идеями с миром.',
    siteName: 'Teletype.in Analog',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Teletype.in Analog',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Teletype.in Analog - Современная блог-платформа',
    description: 'Создавайте, публикуйте и делитесь своими идеями с миром.',
    images: ['/og-image.jpg'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'your-google-verification-code',
    yandex: 'your-yandex-verification-code',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          {children}
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
              success: {
                duration: 3000,
                iconTheme: {
                  primary: '#10b981',
                  secondary: '#fff',
                },
              },
              error: {
                duration: 5000,
                iconTheme: {
                  primary: '#ef4444',
                  secondary: '#fff',
                },
              },
            }}
          />
        </Providers>
      </body>
    </html>
  )
}
