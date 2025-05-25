#!/bin/bash

set -e

echo "Waiting for PostgreSQL to be ready..."

# Wait for PostgreSQL using pg_isready
until python3 -c "
import os
import time
import psycopg2

def is_db_ready():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', '5432')
        )
        cur = conn.cursor()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print('Database connection failed:', e)
        return False

while not is_db_ready():
    print('Waiting for PostgreSQL...')
    time.sleep 2
" ; do
  sleep 2
done

echo "Database is ready."

# Apply migrations
echo "Applying database migrations..."
python3 manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Optional: Create superuser if needed
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    echo "Creating superuser..."
    python3 manage.py createsuperuser \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" \
        --first_name "$DJANGO_SUPERUSER_FIRST_NAME" \
        --last_name "$DJANGO_SUPERUSER_LAST_NAME" \
        --phone "$DJANGO_SUPERUSER_PHONE" \
        --noinput || echo "Superuser creation failed (already exists?)"
fi

# Start server
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 4 friday.wsgi:application