#!/bin/sh
# entrypoint.sh - run migrations, collectstatic and then start passed command
echo "Making migrations and migrating the database. "
python3 manage.py makemigrations --noinput || true
python3 manage.py migrate --noinput || true
python3 manage.py collectstatic --noinput || true
exec "$@"
