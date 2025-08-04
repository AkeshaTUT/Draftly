# 🎨 Teletype.in Analog Frontend

Современный фронтенд для блог-платформы, построенный на Next.js 14 с TypeScript и Tailwind CSS.

## ✨ Особенности

- **Next.js 14** с App Router
- **TypeScript** для типобезопасности
- **Tailwind CSS** для стилизации
- **Dark Mode** поддержка
- **PWA** готовность
- **SEO** оптимизация
- **Responsive** дизайн
- **Accessibility** (a11y) поддержка
- **Performance** оптимизация

## 🚀 Быстрый старт

### Предварительные требования

- Node.js 18+ 
- npm или yarn
- Backend API (см. [backend/README.md](../backend/README.md))

### Установка

1. **Клонируйте репозиторий**
```bash
git clone <repo-url>
cd analog-teletype/frontend
```

2. **Установите зависимости**
```bash
npm install
# или
yarn install
```

3. **Настройте переменные окружения**
```bash
cp .env.example .env.local
```

Отредактируйте `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

4. **Запустите сервер разработки**
```bash
npm run dev
# или
yarn dev
```

Откройте [http://localhost:3000](http://localhost:3000) в браузере.

## 📁 Структура проекта

```
src/
├── app/                    # App Router (Next.js 14)
│   ├── auth/              # Страницы аутентификации
│   ├── dashboard/         # Панель управления
│   ├── explore/           # Просмотр статей
│   ├── layout.tsx         # Корневой layout
│   ├── page.tsx           # Главная страница
│   └── providers.tsx      # Провайдеры контекста
├── components/            # React компоненты
│   ├── layout/           # Layout компоненты
│   └── ui/               # UI компоненты
├── lib/                  # Утилиты и хелперы
│   ├── auth/             # Аутентификация
│   └── utils.ts          # Общие утилиты
├── styles/               # Глобальные стили
├── types/                # TypeScript типы
└── hooks/                # Custom React hooks
```

## 🛠️ Доступные скрипты

```bash
# Разработка
npm run dev              # Запуск dev сервера
npm run build            # Сборка для продакшена
npm run start            # Запуск продакшен сервера

# Линтинг и форматирование
npm run lint             # Проверка ESLint
npm run lint:fix         # Исправление ESLint ошибок
npm run type-check       # Проверка TypeScript типов

# Тестирование
npm run test             # Запуск тестов
npm run test:watch       # Тесты в watch режиме
npm run test:coverage    # Тесты с покрытием

# Storybook
npm run storybook        # Запуск Storybook
npm run build-storybook  # Сборка Storybook
```

## 🎨 Дизайн система

### Цветовая палитра

```css
/* Primary colors */
--primary-50: #eff6ff
--primary-500: #3b82f6
--primary-600: #2563eb
--primary-900: #1e3a8a

/* Neutral colors */
--gray-50: #f9fafb
--gray-500: #6b7280
--gray-900: #111827
```

### Компоненты

- **Button** - Кнопки с различными вариантами
- **Card** - Карточки для контента
- **Input** - Поля ввода
- **Modal** - Модальные окна
- **Toast** - Уведомления

### Утилиты

```css
/* Анимации */
.animate-fade-in
.animate-slide-up
.animate-scale-in

/* Текст */
.text-gradient
.line-clamp-1
.line-clamp-2
.line-clamp-3

/* Скроллбар */
.scrollbar-thin
```

## 🔧 Конфигурация

### Tailwind CSS

Конфигурация находится в `tailwind.config.js`:

```javascript
module.exports = {
  darkMode: ['class'],
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: { /* ... */ },
        // ...
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        // ...
      }
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    // ...
  ]
}
```

### TypeScript

Конфигурация в `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## 📱 PWA поддержка

Приложение готово к PWA с:

- Service Worker
- Web App Manifest
- Offline поддержка
- Push уведомления

### Настройка PWA

1. Обновите `public/manifest.json`
2. Добавьте иконки в `public/`
3. Настройте Service Worker в `src/app/sw.js`

## 🔒 Безопасность

- **CSP** заголовки
- **XSS** защита
- **CSRF** токены
- **Rate limiting**
- **Input validation**

## 📊 Производительность

### Оптимизации

- **Code splitting** - автоматическое разделение кода
- **Image optimization** - оптимизация изображений
- **Font optimization** - оптимизация шрифтов
- **Bundle analysis** - анализ размера бандла

### Метрики

```bash
# Анализ бандла
npm run analyze

# Lighthouse CI
npm run lighthouse
```

## 🧪 Тестирование

### Unit тесты

```bash
npm run test
```

### E2E тесты

```bash
npm run test:e2e
```

### Storybook

```bash
npm run storybook
```

## 📦 Деплой

### Vercel (рекомендуется)

1. Подключите репозиторий к Vercel
2. Настройте переменные окружения
3. Деплой автоматический

### Другие платформы

- **Netlify** - аналогично Vercel
- **Railway** - для полного стека
- **Docker** - для контейнеризации

## 🤝 Вклад в проект

1. Fork проекта
2. Создайте feature ветку (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

### Стандарты кода

- **ESLint** - линтинг JavaScript/TypeScript
- **Prettier** - форматирование кода
- **Husky** - git hooks
- **Commitlint** - стандарты коммитов

## 📚 Документация

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)

## 🐛 Отчеты об ошибках

Используйте [GitHub Issues](https://github.com/your-username/teletype-analog/issues) для отчетов об ошибках.

## 📄 Лицензия

MIT License - см. [LICENSE](../LICENSE) файл.

---

**Создано с ❤️ для современного веб-паблишинга** 