#!/usr/bin/env python3
"""
Скрипт для управления приложением
"""
import os
import sys
import click
from pathlib import Path

# Добавляем путь к приложению
sys.path.append(str(Path(__file__).parent))

from app.core.config import settings
from app.core.database import engine, Base
from app.models import *  # Импортируем все модели


@click.group()
def cli():
    """Утилита для управления Analog Teletype"""
    pass


@cli.command()
def init_db():
    """Инициализация базы данных"""
    import asyncio
    
    async def _init_db():
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            click.echo("База данных инициализирована успешно!")
        except Exception as e:
            click.echo(f"Ошибка инициализации базы данных: {e}")
    
    asyncio.run(_init_db())


@cli.command()
def create_migration():
    """Создание новой миграции"""
    os.system("alembic revision --autogenerate -m 'Auto migration'")


@cli.command()
def migrate():
    """Применение миграций"""
    os.system("alembic upgrade head")


@cli.command()
def rollback():
    """Откат последней миграции"""
    os.system("alembic downgrade -1")


@cli.command()
def show_migrations():
    """Показать статус миграций"""
    os.system("alembic current")
    os.system("alembic history")


@cli.command()
@click.option('--email', prompt='Email администратора')
@click.option('--username', prompt='Username администратора')
@click.option('--password', prompt='Пароль администратора', hide_input=True)
def create_admin(email, username, password):
    """Создание администратора"""
    import asyncio
    from app.services.user_service import UserService
    from app.core.database import AsyncSessionLocal
    from app.models.user import UserRole
    
    async def _create_admin():
        async with AsyncSessionLocal() as db:
            user_service = UserService(db)
            
            # Проверка существования пользователя
            existing_user = await user_service.get_by_email(email)
            if existing_user:
                click.echo(f"Пользователь с email {email} уже существует!")
                return
            
            # Создание администратора
            from app.schemas.user import UserCreate
            
            admin_data = UserCreate(
                email=email,
                username=username,
                password=password,
                first_name="Admin",
                last_name="User"
            )
            
            user = await user_service.create_user(admin_data)
            
            # Установка роли администратора
            await user_service.update_user(str(user.id), {"role": UserRole.ADMIN})
            
            click.echo(f"Администратор {username} создан успешно!")
    
    asyncio.run(_create_admin())


@cli.command()
def run_tests():
    """Запуск тестов"""
    os.system("pytest")


@cli.command()
def format_code():
    """Форматирование кода"""
    os.system("black .")
    os.system("isort .")


@cli.command()
def lint_code():
    """Проверка кода"""
    os.system("flake8 .")
    os.system("mypy .")


@cli.command()
def check_security():
    """Проверка безопасности"""
    os.system("bandit -r app/")


if __name__ == "__main__":
    cli() 