#!/bin/bash
# cp /config-nerdpool/server.py /nerdpool/nerdpool/nerdpool/settings/server.py
# cp /config-nerdpool/wsgi.py /nerdpool/nerdpool/nerdpool/wsgi.py
#cp /config-nerdpool/prodigy.json /nerdpool/nerdpool/prodigy.json
#cp /config-nerdpool/bundle.js /usr/local/lib/python3.8/site-packages/prodigy/static/bundle.js
cp /app/start-nerdpool/default.conf /nginx/conf.d/default.conf
python manage.py collectstatic --noinput --settings=nerdpool.settings.server
python manage.py migrate --settings=nerdpool.settings.server
python manage.py create_server_settings --settings=nerdpool.settings.server
python manage.py enrich_samples --settings=nerdpool.settings.server
python manage.py start_prodigy_servers --settings=nerdpool.settings.server
# htpasswd -bc /nginx/conf.d/.passwd $BASIC_AUTH_USERNAME $BASIC_AUTH_PASSWORD
gunicorn nerdpool.wsgi:application --log-level DEBUG --bind 0.0.0.0:8000
