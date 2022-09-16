# Backend

Backend is written in Python. It requires Python 3.9 or newer. You will need [Poetry](https://python-poetry.org/) version 1.2 or newer to install package and all the dependencies.

## Preparing development environment

Clone Github repo:

    git clone https://github.com/KustoszApp/server

Install dependencies:

    poetry install --with test,dev -E container

## Changing development version configuration

If you want to change the configuration of development version, the best way of doing so is through `settings.local.yaml` (inside `settings` directory). For example, following file would turn on debug-level logging, while ignoring log messages produced by some third-party libraries:

```
default:
  LOGGING__root__level: 'DEBUG'
  LOGGING__loggers__reader__handlers:
    - 'null'
  LOGGING__loggers__readability__handlers:
    - 'null'
  LOGGING__loggers__requests_cache:
    handlers:
      - 'null'
    propagate: False
  LOGGING__loggers__requests:
    handlers:
      - 'null'
    propagate: False
```

## Running current development version

Commands below assume that current virtual environment is active. You can spawn shell with activated virtual environment using:

    poetry shell

Run migrations:

    python manage.py migrate

Create cache tables:

    python manage.py createcachetable

Create user:

    python manage.py createsuperuser --username admin --email admin@example.invalid

Generate authentication token:

    python manage.py drf_create_token admin

Run server:

    python manage.py runserver

Kustosz API server will be available at <http://127.0.0.1:8000/>. You can use curl or [httpx](https://www.python-httpx.org/) to communicate with it. See [](./frontend) for instructions how to run development version of Kustosz frontend.

## Running unit tests

Running unit tests using currently installed Django version and Python version used to create active virtual environment is as simple as:

```
pytest
```

If you want to run unit tests against the matrix of all supported Python and Django versions, then run:
```
nox --non-interactive --session "tests"
```

This will work only if you have binaries for all of the Python versions (e.g. `python3.9` and `python3.10`). You can use [pyenv](https://github.com/pyenv/pyenv) or [asdf](https://asdf-vm.com/) to install them.
