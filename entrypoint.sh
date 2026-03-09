#!/bin/sh

echo "⏳ Waiting for PostgreSQL..."

# Actively probe the DB connection using Python + psycopg2
# More reliable than just trusting the healthcheck alone
until python -c "
import psycopg2, os, sys
try:
    psycopg2.connect(
        dbname=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT'],
    )
    sys.exit(0)
except Exception as e:
    sys.exit(1)
"; do
  echo "  Not ready yet — retrying in 2s..."
  sleep 2
done

echo "✅ PostgreSQL is ready!"

echo "📦 Running migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting server..."
exec "$@"