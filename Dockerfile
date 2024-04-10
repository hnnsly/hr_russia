FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# init db
COPY docker_scritps/create-db.sql /docker-entrypoint-initdb.d/create-db.sql

# для уверенности

COPY bot /app/bot

COPY states /app/states

COPY storage /app/storage

CMD ["python", "app.py"]
