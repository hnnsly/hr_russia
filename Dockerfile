# Используем официальный образ Python 3.11 в качестве базы
FROM python:3.11

# Установка переменной окружения PYTHONUNBUFFERED, которая гарантирует вывод Python без буферизации
ENV PYTHONUNBUFFERED 1

# Установка рабочей директории в /app
WORKDIR /app

# Копируем файлы зависимостей в /app
COPY requirements.txt /app/

# Устанавливаем зависимости из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы из текущей директории в /app в контейнере
COPY . /app/

# Определение переменных окружения для подключения к PostgreSQL
ENV POSTGRES_DB=hr_russia
ENV POSTGRES_USER=andrey115527
ENV POSTGRES_PASSWORD=pasik
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432
ENV BOT_TOKEN=6958631398:AAHwdQ9tdS-fiQ2NnFZ9QVyhqCc3JUTRbJQ

# Установка переменной окружения для указания приложению на использование PostgreSQL
ENV DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB

# Копируем SQL-скрипт для инициализации базы данных
COPY init-db.sql /docker-entrypoint-initdb.d/init-db.sql

# Команда для запуска приложения
CMD ["python", "app.py"]
