import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * Объединяет классы CSS с помощью clsx и tailwind-merge
 * Позволяет правильно объединять Tailwind классы без конфликтов
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Форматирует дату в читаемый вид
 */
export function formatDate(date: string | Date, options?: Intl.DateTimeFormatOptions): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date
  
  const defaultOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    ...options
  }
  
  return dateObj.toLocaleDateString('ru-RU', defaultOptions)
}

/**
 * Форматирует относительное время (например, "2 часа назад")
 */
export function formatRelativeTime(date: string | Date): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date
  const now = new Date()
  const diffInSeconds = Math.floor((now.getTime() - dateObj.getTime()) / 1000)
  
  if (diffInSeconds < 60) {
    return 'только что'
  }
  
  const diffInMinutes = Math.floor(diffInSeconds / 60)
  if (diffInMinutes < 60) {
    return `${diffInMinutes} ${getPluralForm(diffInMinutes, 'минуту', 'минуты', 'минут')} назад`
  }
  
  const diffInHours = Math.floor(diffInMinutes / 60)
  if (diffInHours < 24) {
    return `${diffInHours} ${getPluralForm(diffInHours, 'час', 'часа', 'часов')} назад`
  }
  
  const diffInDays = Math.floor(diffInHours / 24)
  if (diffInDays < 7) {
    return `${diffInDays} ${getPluralForm(diffInDays, 'день', 'дня', 'дней')} назад`
  }
  
  const diffInWeeks = Math.floor(diffInDays / 7)
  if (diffInWeeks < 4) {
    return `${diffInWeeks} ${getPluralForm(diffInWeeks, 'неделю', 'недели', 'недель')} назад`
  }
  
  const diffInMonths = Math.floor(diffInDays / 30)
  if (diffInMonths < 12) {
    return `${diffInMonths} ${getPluralForm(diffInMonths, 'месяц', 'месяца', 'месяцев')} назад`
  }
  
  const diffInYears = Math.floor(diffInDays / 365)
  return `${diffInYears} ${getPluralForm(diffInYears, 'год', 'года', 'лет')} назад`
}

/**
 * Возвращает правильную форму множественного числа для русского языка
 */
function getPluralForm(count: number, one: string, few: string, many: string): string {
  const mod10 = count % 10
  const mod100 = count % 100
  
  if (mod100 >= 11 && mod100 <= 19) {
    return many
  }
  
  if (mod10 === 1) {
    return one
  }
  
  if (mod10 >= 2 && mod10 <= 4) {
    return few
  }
  
  return many
}

/**
 * Форматирует число с разделителями тысяч
 */
export function formatNumber(num: number): string {
  return new Intl.NumberFormat('ru-RU').format(num)
}

/**
 * Сокращает число до читаемого вида (например, 1.2K, 1.5M)
 */
export function formatCompactNumber(num: number): string {
  if (num < 1000) {
    return num.toString()
  }
  
  if (num < 1000000) {
    return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K'
  }
  
  return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M'
}

/**
 * Генерирует случайный ID
 */
export function generateId(): string {
  return Math.random().toString(36).substring(2) + Date.now().toString(36)
}

/**
 * Дебаунс функция для отложенного выполнения
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout
  
  return (...args: Parameters<T>) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

/**
 * Троттлинг функция для ограничения частоты выполнения
 */
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean
  
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

/**
 * Копирует текст в буфер обмена
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(text)
      return true
    } else {
      // Fallback для старых браузеров
      const textArea = document.createElement('textarea')
      textArea.value = text
      document.body.appendChild(textArea)
      textArea.select()
      document.execCommand('copy')
      document.body.removeChild(textArea)
      return true
    }
  } catch (error) {
    console.error('Ошибка копирования в буфер обмена:', error)
    return false
  }
}

/**
 * Проверяет, является ли строка валидным email
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Проверяет, является ли строка валидным URL
 */
export function isValidUrl(url: string): boolean {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

/**
 * Извлекает домен из URL
 */
export function extractDomain(url: string): string {
  try {
    const urlObj = new URL(url)
    return urlObj.hostname
  } catch {
    return url
  }
}

/**
 * Создает slug из строки
 */
export function createSlug(text: string): string {
  return text
    .toLowerCase()
    .replace(/[а-яё]/g, (char) => {
      const map: { [key: string]: string } = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
      }
      return map[char] || char
    })
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .trim()
}

/**
 * Обрезает текст до указанной длины с многоточием
 */
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) {
    return text
  }
  return text.slice(0, maxLength).trim() + '...'
}

/**
 * Получает инициалы из имени
 */
export function getInitials(name: string): string {
  return name
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

/**
 * Проверяет, поддерживает ли браузер определенную функцию
 */
export function isSupported(feature: string): boolean {
  if (typeof window === 'undefined') return false
  
  const features: { [key: string]: boolean } = {
    'clipboard': !!navigator.clipboard,
    'localStorage': !!window.localStorage,
    'sessionStorage': !!window.sessionStorage,
    'serviceWorker': 'serviceWorker' in navigator,
    'pushManager': 'PushManager' in window,
    'notifications': 'Notification' in window,
    'geolocation': 'geolocation' in navigator,
    'webGL': !!window.WebGLRenderingContext,
    'webP': (() => {
      const canvas = document.createElement('canvas')
      canvas.width = 1
      canvas.height = 1
      return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0
    })()
  }
  
  return features[feature] || false
}

/**
 * Получает размер файла в читаемом виде
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Б'
  
  const k = 1024
  const sizes = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * Задержка выполнения
 */
export function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Проверяет, находится ли элемент в области видимости
 */
export function isElementInViewport(element: Element): boolean {
  const rect = element.getBoundingClientRect()
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  )
}

/**
 * Плавная прокрутка к элементу
 */
export function scrollToElement(element: Element | string, offset: number = 0): void {
  const target = typeof element === 'string' ? document.querySelector(element) : element
  if (!target) return
  
  const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset
  window.scrollTo({
    top: targetPosition,
    behavior: 'smooth'
  })
}
