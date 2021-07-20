#!/bin/bash
 if [ -z "$VCAP_APP_PORT" ]; then
    SERVER_PORT=8000;
 else
    SERVER_PORT="$VCAP_APP_PORT";
 fi

 echo "fake migrations perfocal"
 python manage.py migrate --fake perfocal zero

 echo "fake migrations maintenance"
 python manage.py migrate --fake maintenance zero

 echo "show migrations"
 python manage.py showmigrations

 echo "delete migrations"
 find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

 echo "make migrations"
 python manage.py makemigrations

 echo "migrate"
 python manage.py migrate --fake-initial

  echo "make migrations"
 python manage.py makemigrations

 echo "sqlmigrate"
 python manage.py sqlmigrate 0001

 echo "inspect"
 python manage.py inspectdb
 > perfocal/models.py

 echo "collectstatic"
 python manage.py collectstatic --noinput

  echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'smita.gadade@preciseindsol.com', '1234')" | python manage.py shell

 echo port is "$SERVER_PORT"

# echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@whizzy.io', 'password')" | python manage.py shell
# echo "from django.contrib.auth.models import User; if not User.objects.filter(username='admin').exists():...
#   User.objects.create_superuser('admin', 'admin@whizzy.io', 'password') EOF" | python manage.py shell

 echo [$0] Starting Django Server...
 python manage.py runserver 0.0.0.0:"$SERVER_PORT"

