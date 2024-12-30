#!/bin/bash

# Verify that Postgres is healthy before applying the migrations and running the Django development server
if [ "$DATABASE_ENGINE" = "postgres" ]; then echo "Waiting for postgres..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL is accepting connections"
fi

echo "Apply database migrations"
python manage.py migrate

echo "Starting server"
python manage.py runserver 0.0.0.0:8000
