#!/bin/bash

cd /code/app/tilkku

python manage.py migrate --noinput
python manage.py initadmin
python manage.py runserver 0.0.0.0:8000