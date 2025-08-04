@echo off
echo Installing fixed dependencies for Analog Teletype Backend...
echo.

REM Проверяем наличие Python
py --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.11+ and try again.
    pause
    exit /b 1
)

REM Обновляем pip
echo Updating pip...
py -m pip install --upgrade pip

REM Устанавливаем исправленные зависимости
echo Installing dependencies...
py -m pip install -r requirements-fixed.txt

REM Проверяем установку
echo.
echo Checking installation...
py -c "import fastapi, pydantic, sqlalchemy; print('✅ All core packages installed successfully')"

echo.
echo Installation completed! You can now run:
echo   py run.py
pause 