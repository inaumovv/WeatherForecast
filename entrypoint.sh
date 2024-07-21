#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then

    echo "Рано..."


    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "Пора!"
fi


python manage.py makemigrations
python manage.py migrate

exec "$@"
