@echo off
echo Starting Analog Teletype Backend...
echo.

REM Проверяем наличие Python
py --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.11+ and try again.
    pause
    exit /b 1
)

REM Проверяем наличие .env файла
if not exist ".env" (
    echo Creating .env file from template...
    copy env.example .env
    echo Please edit .env file with your settings before running again.
    pause
    exit /b 1
)

REM Устанавливаем зависимости если нужно
if not exist "venv" (
    echo Creating virtual environment...
    py -m venv venv
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    py -m pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Инициализируем базу данных
echo Initializing database...
py manage.py init_db

REM Запускаем приложение
echo Starting FastAPI application...
py run.py

pause 