# Analog Teletype Backend Startup Script
Write-Host "🚀 Starting Analog Teletype Backend..." -ForegroundColor Green
Write-Host ""

# Проверяем наличие Python
try {
    $pythonVersion = py --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python not found. Please install Python 3.11+ and try again." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Проверяем наличие .env файла
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
    Write-Host "⚠️  Please edit .env file with your settings before running again." -ForegroundColor Yellow
    Write-Host "   You can use: notepad .env" -ForegroundColor Cyan
    Read-Host "Press Enter to exit"
    exit 1
}

# Создаем виртуальное окружение если нужно
if (-not (Test-Path "venv")) {
    Write-Host "🔧 Creating virtual environment..." -ForegroundColor Yellow
    py -m venv venv
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
    py -m pip install -r requirements.txt
} else {
    Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
}

# Инициализируем базу данных
Write-Host "🗄️  Initializing database..." -ForegroundColor Yellow
py manage.py init_db

# Запускаем приложение
Write-Host "🌐 Starting FastAPI application..." -ForegroundColor Green
Write-Host "   API will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "   Swagger docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "   Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

py run.py 