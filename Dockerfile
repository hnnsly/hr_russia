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

# токен бота
ENV BOT_TOKEN=6958631398:AAHwdQ9tdS-fiQ2NnFZ9QVyhqCc3JUTRbJQ
ENV POSTGRES_DB=hr_russia
ENV POSTGRES_USER=andrey115527
ENV POSTGRES_PASSWORD=pasik
#ENV PGADMIN_LOGIN=admin@admin.com
#ENV PGADMIN_PASSWORD=root

# Копируем SQL-скрипт для инициализации базы данных
COPY docker_scritps/create-db.sql /docker-entrypoint-initdb.d/create-db.sql

# Копируем папку bot в контейнер
COPY bot /app/bot

# Копируем папку states в контейнер
COPY states /app/states

# Копируем папку storage в контейнер
COPY storage /app/storage

# Команда для запуска приложения
CMD ["python", "app.py"]
