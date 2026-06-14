#!/bin/sh

echo "Waiting for PostgreSQL..."

while ! python -c "import socket; socket.create_connection(('db', 5432), timeout=2)"; do
  sleep 1
done

echo "PostgreSQL is ready"

python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"