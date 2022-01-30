# Backend

Clone Github repo:

    https://github.com/KustoszApp/server

Install dependencies:

    poetry install

Run migrations:

    python manage.py migrate

Create cache tables:

    python manage.py createcachetable

Create user:

    python manage.py createsuperuser --username admin --email admin@example.invalid

Run server:

    python manage.py runserver
