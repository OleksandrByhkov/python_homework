#!/bin/sh
set -e

if [ "${SKIP_MIGRATIONS:-False}" != "True" ]; then
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput
fi

exec "$@"