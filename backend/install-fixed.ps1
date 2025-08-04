# Install Fixed Dependencies for Analog Teletype Backend
Write-Host "🔧 Installing fixed dependencies for Analog Teletype Backend..." -ForegroundColor Green
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

# Обновляем pip
Write-Host "📦 Updating pip..." -ForegroundColor Yellow
py -m pip install --upgrade pip

# Устанавливаем исправленные зависимости
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
py -m pip install -r requirements-fixed.txt

# Проверяем установку
Write-Host ""
Write-Host "🔍 Checking installation..." -ForegroundColor Yellow
try {
    py -c "import fastapi, pydantic, sqlalchemy; print('✅ All core packages installed successfully')"
    Write-Host "✅ Installation completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Installation failed. Please check the error messages above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🚀 You can now run:" -ForegroundColor Cyan
Write-Host "   py run.py" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to continue" 