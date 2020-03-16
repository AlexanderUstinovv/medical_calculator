#!/bin/sh

if [ "$SQL_DATABASE" = "medical_calculator" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python /app/manage.py flush --no-input
python /app/manage.py migrate
python /app/manage.py collectstatic --no-input --clear

gunicorn medical_calculator.wsgi:application --bind 0.0.0.0:8000

exec "$@"