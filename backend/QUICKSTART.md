# 🚀 Быстрый старт на Windows

## Вариант 1: Автоматический запуск (рекомендуется)

### PowerShell (рекомендуется)
```powershell
# В папке backend
.\start.ps1
```

### Command Prompt
```cmd
# В папке backend
start.bat
```

## Вариант 1.5: Исправленная установка (если есть проблемы)

Если у вас возникли проблемы с зависимостями, используйте исправленные скрипты:

### PowerShell
```powershell
# В папке backend
.\install-fixed.ps1
```

### Command Prompt
```cmd
# В папке backend
install-fixed.bat
```

## Вариант 2: Ручной запуск

### 1. Установка зависимостей
```powershell
py -m pip install -r requirements.txt
```

### 2. Создание .env файла
```powershell
copy env.example .env
# Отредактируйте .env файл под ваши настройки
```

### 3. Инициализация базы данных
```powershell
py manage.py init_db
```

### 4. Запуск приложения
```powershell
py run.py
```

## 🌐 Доступ к API

После запуска:
- **API:** http://localhost:8000
- **Swagger документация:** http://localhost:8000/docs
- **ReDoc документация:** http://localhost:8000/redoc

## 🔧 Основные команды

```powershell
# Создать админа
py manage.py create_admin

# Запустить тесты
py manage.py run_tests

# Форматировать код
py manage.py format_code

# Проверить код
py manage.py lint_code
```

## 🐳 Docker (альтернатива)

Если у вас установлен Docker:

```powershell
# Запустить все сервисы
docker-compose up -d

# Только backend
docker-compose up backend
```

## ❗ Возможные проблемы

### Python не найден
Установите Python 3.11+ с официального сайта: https://python.org

### Ошибки с зависимостями
```powershell
# Обновить pip
py -m pip install --upgrade pip

# Использовать исправленные зависимости
py -m pip install -r requirements-fixed.txt

# Или переустановить зависимости
py -m pip install -r requirements.txt --force-reinstall
```

### Проблемы с базой данных
Убедитесь, что PostgreSQL запущен и доступен по адресу из .env файла.

### Проблемы с правами выполнения скриптов
```powershell
# Разрешить выполнение скриптов
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
``` 