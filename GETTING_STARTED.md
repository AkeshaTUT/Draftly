# 🚀 Инструкции по запуску Teletype.in Analog

## Быстрый старт с Docker

1. **Скопируйте переменные окружения:**
```bash
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
```

2. **Запустите проект:**
```bash
docker-compose up -d
```

3. **Откройте в браузере:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Разработка без Docker

### Backend (FastAPI)

1. **Создайте виртуальное окружение:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Настройте базу данных:**
```bash
# Запустите PostgreSQL и Redis локально
# Обновите DATABASE_URL и REDIS_URL в .env
```

4. **Запустите сервер:**
```bash
uvicorn app.main:app --reload
```

### Frontend (Next.js)

1. **Установите зависимости:**
```bash
cd frontend
npm install
```

2. **Запустите dev сервер:**
```bash
npm run dev
```

## Доступные команды в VS Code

Нажмите `Ctrl+Shift+P` и выберите `Tasks: Run Task`:

- **Start Teletype.in Analog (Full Stack)** - Запуск через Docker
- **Stop Teletype.in Analog** - Остановка всех сервисов
- **Backend Dev Server** - Запуск только backend
- **Frontend Dev Server** - Запуск только frontend
- **Install Backend Dependencies** - Установка Python пакетов
- **Install Frontend Dependencies** - Установка npm пакетов

## Настройка для продакшена

1. **Backend .env:**
```env
DATABASE_URL=postgresql://user:pass@your-db-host:5432/db_name
REDIS_URL=redis://your-redis-host:6379
SECRET_KEY=your-super-secret-key-minimum-32-characters
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://yourdomain.com
```

2. **Frontend .env.local:**
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_APP_URL=https://yourdomain.com
```

## Структура проекта

```
📦 Teletype.in Analog
├── 🐍 backend/                 # FastAPI приложение
│   ├── app/
│   │   ├── api/                # REST API endpoints
│   │   ├── core/               # Конфигурация, безопасность
│   │   ├── models/             # SQLAlchemy модели
│   │   ├── schemas/            # Pydantic схемы
│   │   ├── services/           # Бизнес-логика
│   │   └── main.py
│   ├── alembic/                # Миграции БД
│   └── requirements.txt
├── ⚛️ frontend/                # Next.js приложение
│   ├── src/
│   │   ├── app/                # App Router
│   │   ├── components/         # React компоненты
│   │   └── lib/                # Утилиты и хуки
│   ├── public/                 # Статические файлы
│   └── package.json
├── 🐳 docker-compose.yml       # Docker конфигурация
└── 📖 README.md
```

## Основные функции

✅ **Готово:**
- Структура проекта
- Аутентификация (JWT)
- Модели данных (User, Article, Comment, etc.)
- Docker конфигурация
- PWA поддержка
- Безопасность (CORS, rate limiting)

🚧 **В разработке:**
- API endpoints реализация
- React компоненты
- Markdown редактор
- Файловые загрузки
- Telegram бот
- Email уведомления

## Технологии

**Backend:**
- FastAPI (Python 3.11+)
- SQLAlchemy + Alembic
- PostgreSQL + Redis
- Celery + RabbitMQ
- JWT аутентификация

**Frontend:**
- Next.js 14 (App Router)
- React 18 + TypeScript
- Tailwind CSS
- Shadcn/UI компоненты
- PWA поддержка

**DevOps:**
- Docker + Docker Compose
- GitHub Actions (CI/CD)
- Sentry (мониторинг)

---

🎉 **Готово к разработке!** Начните с запуска `docker-compose up -d` или используйте VS Code таски.
