#!/usr/bin/env python3
"""
Скрипт для запуска FastAPI приложения
"""
import uvicorn
import os
import sys
from pathlib import Path

# Добавляем путь к приложению
sys.path.append(str(Path(__file__).parent))

from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning",
        access_log=True,
    ) 