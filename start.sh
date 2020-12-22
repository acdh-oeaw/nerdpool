#!/bin/bash
python manage.py collectstatic --noinput --settings=nerdpool.settings.server
python manage.py migrate --settings=nerdpool.settings.server
python manage.py create_server_settings --settings=nerdpool.settings.server
python manage.py enrich_samples --settings=nerdpool.settings.server
python manage.py start_prodigy_servers --settings=nerdpool.settings.server
htpasswd -bc /etc/nginx/conf.d/.passwd $BASIC_AUTH_USERNAME $BASIC_AUTH_PASSWORD
gunicorn nerdpool.wsgi --user www-data --bind 0.0.0.0:8000 --workers 3 & nginx -g "daemon off;"
