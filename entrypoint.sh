#!/usr/bin/env bash

python manage.py makemigrations cdb_rest
python manage.py migrate
mkdir -p static/
python manage.py collectstatic --noinput

if [ "$1" == "django" ]; then
    exec python manage.py runserver 0.0.0.0:8080
elif [ "$1" == "apache" ]; then
    exec /usr/sbin/apachectl -DFOREGROUND
else
    exec "$@"
fi
