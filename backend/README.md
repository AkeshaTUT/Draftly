# Backend - Analog Teletype

Backend часть профессионального аналога Teletype.in

## 🚀 Быстрый старт

### Windows (PowerShell)

1. **Установка зависимостей:**
```powershell
py -m pip install -r requirements.txt
```

2. **Создание .env файла:**
```powershell
copy env.example .env
# Отредактировать настройки в .env файле
```

3. **Инициализация базы данных:**
```powershell
py manage.py init_db
```

4. **Запуск приложения:**
```powershell
py run.py
```

### Linux/Mac

1. **Установка зависимостей:**
```bash
pip install -r requirements.txt
```

2. **Создание .env файла:**
```bash
cp env.example .env
# Отредактировать настройки в .env файле
```

3. **Инициализация базы данных:**
```bash
python manage.py init_db
```

4. **Запуск приложения:**
```bash
python run.py
```

## 🐳 Docker

### Запуск всех сервисов:
```bash
docker-compose up -d
```

### Только backend:
```bash
docker-compose up backend
```

## 📋 Доступные команды

### Управление базой данных:
```powershell
# Windows
py manage.py init_db          # Инициализация БД
py manage.py create_migration # Создать миграцию
py manage.py migrate          # Применить миграции
py manage.py rollback         # Откатить миграцию
py manage.py show_migrations  # Показать статус миграций
```

### Разработка:
```powershell
# Windows
py manage.py run_tests        # Запуск тестов
py manage.py format_code      # Форматирование кода
py manage.py lint_code        # Проверка кода
py manage.py check_security   # Проверка безопасности
```

### Администрирование:
```powershell
# Windows
py manage.py create_admin     # Создать админа
```

## 🌐 API Endpoints

После запуска API будет доступен по адресу:
- **Swagger документация:** http://localhost:8000/docs
- **ReDoc документация:** http://localhost:8000/redoc
- **API Base URL:** http://localhost:8000/api/v1/

### Основные эндпоинты:
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход
- `GET /api/v1/auth/me` - Информация о пользователе
- `GET /api/v1/users/{username}` - Профиль пользователя
- `POST /api/v1/articles/` - Создание статьи
- `GET /api/v1/articles/` - Список статей

## 🔧 Настройка

### Переменные окружения (.env):

```env
# Основные настройки
DEBUG=True
SECRET_KEY=your-secret-key-here

# База данных
DATABASE_URL=postgresql://user:password@localhost:5432/teletype
ASYNC_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/teletype

# Redis
REDIS_URL=redis://localhost:6379/0

# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Telegram
TELEGRAM_BOT_TOKEN=your-telegram-bot-token

# Платежи
YOOMONEY_SHOP_ID=your-yoomoney-shop-id
YOOMONEY_SECRET_KEY=your-yoomoney-secret
KASPI_MERCHANT_ID=your-kaspi-merchant-id
KASPI_API_KEY=your-kaspi-api-key
```

## 📁 Структура проекта

```
backend/
├── app/
│   ├── api/                 # API endpoints
│   │   └── v1/
│   │       └── endpoints/
│   ├── core/               # Основные настройки
│   ├── models/             # Модели БД
│   ├── schemas/            # Pydantic схемы
│   ├── services/           # Бизнес-логика
│   ├── tasks/              # Celery задачи
│   └── templates/          # Email шаблоны
├── alembic/                # Миграции БД
├── tests/                  # Тесты
├── requirements.txt        # Зависимости
├── manage.py              # CLI утилиты
└── run.py                 # Запуск приложения
```

## 🧪 Тестирование

```powershell
# Windows
py -m pytest               # Запуск всех тестов
py -m pytest -v            # Подробный вывод
py -m pytest -k "auth"     # Тесты с маркером
py -m pytest --cov=app     # С покрытием кода
```

## 🔍 Отладка

### Логирование:
Логи записываются в `logs/` директорию с использованием `structlog`.

### Отладка в IDE:
1. Установите точки останова в коде
2. Запустите `py run.py` в режиме отладки
3. Или используйте VS Code/PyCharm debugger

## 🚀 Продакшн

### Подготовка к деплою:
1. Установите `DEBUG=False` в .env
2. Настройте продакшн базу данных
3. Настройте Redis и RabbitMQ
4. Установите SSL сертификаты
5. Настройте reverse proxy (nginx)

### Мониторинг:
- **Sentry** для отслеживания ошибок
- **Prometheus** для метрик
- **Grafana** для дашбордов

## 📚 Документация

- [FastAPI документация](https://fastapi.tiangolo.com/)
- [SQLAlchemy документация](https://docs.sqlalchemy.org/)
- [Celery документация](https://docs.celeryproject.org/)
- [Alembic документация](https://alembic.sqlalchemy.org/)

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для фичи
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📄 Лицензия

MIT License 