web: python leidos_project/manage.py runserver 0.0.0.0:$PORT
release: python manage.py migrate
web: gunicorn leidos_app.wsgi --log-file -
