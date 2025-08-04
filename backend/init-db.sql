-- Инициализация базы данных PostgreSQL

-- Создание расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Создание индексов для полнотекстового поиска
-- (будет добавлено через Alembic миграции)
