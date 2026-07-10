#!/bin/bash
set -e

python manage.py migrate --noinput
python manage.py setup_admin

exec gunicorn blog.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --access-logfile - \
    --error-logfile -
