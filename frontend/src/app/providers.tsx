'use client'

import { ThemeProvider } from 'next-themes'
import { AuthProvider } from '@/lib/auth/AuthProvider'
import { SWRConfig } from 'swr'
import { useEffect, useState } from 'react'

interface ProvidersProps {
  children: React.ReactNode
}

export function Providers({ children }: ProvidersProps) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return <div className="min-h-screen bg-white dark:bg-gray-950" />
  }

  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      <SWRConfig
        value={{
          fetcher: (url: string) => fetch(url).then((res) => res.json()),
          revalidateOnFocus: false,
          revalidateOnReconnect: true,
          errorRetryCount: 3,
          errorRetryInterval: 5000,
        }}
      >
        <AuthProvider>
          <div className="min-h-screen bg-white text-gray-900 dark:bg-gray-950 dark:text-gray-100">
            {children}
          </div>
        </AuthProvider>
      </SWRConfig>
    </ThemeProvider>
  )
}
