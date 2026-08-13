#!/bin/sh

echo "Waiting for PostgreSQL..."
echo "POSTGRES_HOST=$POSTGRES_HOST"
echo "POSTGRES_PORT=$POSTGRES_PORT"

while ! python -c "import os, socket; socket.create_connection((os.getenv('POSTGRES_HOST'), int(os.getenv('POSTGRES_PORT', '5432'))), timeout=2)"; do
    sleep 1
done

echo "PostgreSQL is ready"

python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"