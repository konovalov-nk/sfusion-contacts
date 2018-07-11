#!/usr/bin/env sh

# Wait for Postgres to start
function postgres_ready() {
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="db")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 3
done

python manage.py migrate
python manage.py collectstatic --no-input

gunicorn project.wsgi -b 0.0.0.0:8005 --reload