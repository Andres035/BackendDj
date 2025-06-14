#C:\Users\benit\Downloads\Tienda-Online-main\BackendDj\entrypoint.sh

#!/bin/sh
#!/bin/sh

echo 'Applying migrations...'
python manage.py migrate

echo 'Collecting static files...'
python manage.py collectstatic --no-input

echo 'Running server...'
gunicorn --env DJANGO_SETTINGS_MODULE=main.settings main.wsgi:application --bind 0.0.0.0:$PORT
