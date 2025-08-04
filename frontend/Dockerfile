FROM node:18-alpine

# Установка зависимостей системы
RUN apk add --no-cache libc6-compat

# Создание рабочей директории
WORKDIR /app

# Копирование package.json и package-lock.json
COPY package*.json ./

# Установка зависимостей
RUN npm ci --only=production

# Копирование исходного кода
COPY . .

# Установка переменных окружения
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Сборка приложения
RUN npm run build

# Экспорт порта
EXPOSE 3000

# Команда запуска
CMD ["npm", "start"]
