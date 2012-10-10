web: python manage.py collectstatic --noinput; newrelic-admin run-program gunicorn ausbildung.wsgi -k gevent -b 0.0.0.0:$PORT
