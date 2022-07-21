#!/bin/bash

cd /code/tilkku

django-admin compilemessages
python manage.py makemigrations --noinput
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput
python manage.py loaddata tilkku/fixtures.yml

#python manage.py runserver 0.0.0.0:8000
gunicorn tilkku.asgi:application --bind 0.0.0.0:8000 --workers 4