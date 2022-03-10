#!/usr/bin/env bash

RETRIES=6

until python manage.py check --database default > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for database server, $((RETRIES--)) remaining attempts..."
  sleep 10
done

python manage.py makemigrations cdb_rest
python manage.py migrate
mkdir -p static/
python manage.py collectstatic --noinput

if [ "$1" == "django" ]; then
    exec python manage.py runserver 0.0.0.0:8080
elif [ "$1" == "nginx" ]; then
    /usr/sbin/nginx -c /npdb/nginx_django_host.conf
    gunicorn nopayloaddb.wsgi:application --bind 0.0.0.0:8088
elif [ "$1" == "apache" ]; then
    exec /usr/sbin/apachectl -DFOREGROUND
else
    exec "$@"
fi
