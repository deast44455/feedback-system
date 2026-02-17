#!/bin/bash

# Ожидание доступности PostgreSQL
echo "Ожидание доступности PostgreSQL..."
while ! pg_isready -h $DATABASE_HOST -p $DATABASE_PORT -U $DATABASE_USER > /dev/null 2>&1; do
  sleep 1
done
echo "PostgreSQL готов!"

# Применение миграций
echo "Применение миграций базы данных..."
python manage.py migrate --noinput

# Сбор статических файлов
echo "Сбор статических файлов..."
python manage.py collectstatic --noinput

echo "Запуск сервера..."
exec "$@"
