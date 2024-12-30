#!/bin/bash

# Verify that Postgres is healthy before applying the migrations and running the Django development server
if [ "$DATABASE_ENGINE" = "postgres" ]; then echo "Waiting for postgres..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL is accepting connections"
fi

echo "Applying database migrations"
python manage.py migrate

echo "Collecting static files"
python manage.py collectstatic --noinput

echo "Starting server"

# Change the --forwarded-allow-ips parameter to the actual IP address of the reverse proxy server
# or ensure that gunicorn is only accessible from the reverse proxy server
/usr/local/bin/gunicorn sams.wsgi:application --workers 2 --forwarded-allow-ips="*" --bind :8000
