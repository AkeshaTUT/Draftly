import { useState, useCallback } from 'react'
import { ApiResponse, ApiError } from '@/types'
import toast from 'react-hot-toast'

interface UseApiOptions<T> {
  onSuccess?: (data: T) => void
  onError?: (error: ApiError) => void
  showToast?: boolean
}

interface UseApiReturn<T> {
  data: T | null
  loading: boolean
  error: ApiError | null
  execute: (...args: any[]) => Promise<T | null>
  reset: () => void
}

export function useApi<T = any>(
  apiCall: (...args: any[]) => Promise<ApiResponse<T>>,
  options: UseApiOptions<T> = {}
): UseApiReturn<T> {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<ApiError | null>(null)

  const execute = useCallback(
    async (...args: any[]): Promise<T | null> => {
      setLoading(true)
      setError(null)

      try {
        const response = await apiCall(...args)
        
        if (response.success) {
          setData(response.data)
          options.onSuccess?.(response.data)
          
          if (options.showToast && response.message) {
            toast.success(response.message)
          }
          
          return response.data
        } else {
          throw new Error(response.message || 'Произошла ошибка')
        }
      } catch (err: any) {
        const apiError: ApiError = {
          detail: err.message || 'Неизвестная ошибка',
          code: err.code,
          field: err.field
        }
        
        setError(apiError)
        options.onError?.(apiError)
        
        if (options.showToast !== false) {
          toast.error(apiError.detail)
        }
        
        return null
      } finally {
        setLoading(false)
      }
    },
    [apiCall, options]
  )

  const reset = useCallback(() => {
    setData(null)
    setLoading(false)
    setError(null)
  }, [])

  return {
    data,
    loading,
    error,
    execute,
    reset
  }
}

// Специализированные хуки для конкретных API вызовов
export function useAuth() {
  const login = useApi(
    async (email: string, password: string) => {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      return response.json()
    },
    { showToast: true }
  )

  const register = useApi(
    async (userData: any) => {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      })
      return response.json()
    },
    { showToast: true }
  )

  const logout = useApi(
    async () => {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/logout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
      return response.json()
    },
    { showToast: true }
  )

  return { login, register, logout }
}

export function useArticles() {
  const getArticles = useApi(
    async (params?: any) => {
      const searchParams = new URLSearchParams(params)
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/articles?${searchParams}`
      )
      return response.json()
    }
  )

  const getArticle = useApi(
    async (slug: string) => {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/articles/${slug}`
      )
      return response.json()
    }
  )

  const createArticle = useApi(
    async (articleData: any) => {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/articles`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(articleData)
      })
      return response.json()
    },
    { showToast: true }
  )

  const updateArticle = useApi(
    async (id: number, articleData: any) => {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/articles/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(articleData)
      })
      return response.json()
    },
    { showToast: true }
  )

  const deleteArticle = useApi(
    async (id: number) => {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/articles/${id}`, {
        method: 'DELETE'
      })
      return response.json()
    },
    { showToast: true }
  )

  return {
    getArticles,
    getArticle,
    createArticle,
    updateArticle,
    deleteArticle
  }
}

export function useUsers() {
  const getUser = useApi(
    async (username: string) => {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/users/${username}`
      )
      return response.json()
    }
  )

  const getUserArticles = useApi(
    async (username: string, params?: any) => {
      const searchParams = new URLSearchParams(params)
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/users/${username}/articles?${searchParams}`
      )
      return response.json()
    }
  )

  const followUser = useApi(
    async (username: string) => {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/users/${username}/follow`,
        { method: 'POST' }
      )
      return response.json()
    },
    { showToast: true }
  )

  const unfollowUser = useApi(
    async (username: string) => {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/users/${username}/follow`,
        { method: 'DELETE' }
      )
      return response.json()
    },
    { showToast: true }
  )

  return {
    getUser,
    getUserArticles,
    followUser,
    unfollowUser
  }
}

export function useComments() {
  const getComments = useApi(
    async (articleId: number, params?: any) => {
      const searchParams = new URLSearchParams(params)
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/articles/${articleId}/comments?${searchParams}`
      )
      return response.json()
    }
  )

  const createComment = useApi(
    async (articleId: number, content: string) => {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/articles/${articleId}/comments`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content })
        }
      )
      return response.json()
    },
    { showToast: true }
  )

  const updateComment = useApi(
    async (commentId: number, content: string) => {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/comments/${commentId}`,
        {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content })
        }
      )
      return response.json()
    },
    { showToast: true }
  )

  const deleteComment = useApi(
    async (commentId: number) => {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/comments/${commentId}`,
        { method: 'DELETE' }
      )
      return response.json()
    },
    { showToast: true }
  )

  return {
    getComments,
    createComment,
    updateComment,
    deleteComment
  }
}

export function useLikes() {
  const likeArticle = useApi(
    async (articleId: number) => {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/articles/${articleId}/like`,
        { method: 'POST' }
      )
      return response.json()
    }
  )

  const unlikeArticle = useApi(
    async (articleId: number) => {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/articles/${articleId}/like`,
        { method: 'DELETE' }
      )
      return response.json()
    }
  )

  return {
    likeArticle,
    unlikeArticle
  }
} 