# VPS (Raspberry Pi, DigitalOcean Droplet) (Work In Progress)

:::{admonition} This page is long
:class: warning

This page is intentionally detailed and quite long. The goal is to discuss various tradeoffs involved in deploying Kustosz. You are advised to familiarize yourself with entire document before taking any action.
:::

## Prerequisites

Kustosz is web application. You probably want a dedicated (sub)domain that supports secure HTTPS connection. That part of setup is out of scope for this guide.

There are few dependencies that you absolutely must meet:

* Python 3.9 or newer
* WSGI-compatible web server, like Apache with mod_wsgi or Nginx
* Ability to execute arbitrary commands in the context of server
* Ability to start your own long-running processes (needed by Celery worker)
* At least 256 MiB of memory

While not required, we also recommend:

* [PostgreSQL](https://www.postgresql.org/) database server
* [Redis](https://redis.io/) as Celery transport

## Overview of Kustosz installation



## Prepare Kustosz server environment

Create Kustosz base directory. This is where you will put settings, and where Kustosz will store cache and SQLite database file.

```
mkdir ~/kustosz_home
```

Create environment variables required by Kustosz. You need to ensure they are set for all processes that involve Kustosz, e.g. Celery or cron job. You might want to add them to `~/.bash_profile`.

```
export ENV_FOR_DYNACONF="production"
export DJANGO_SETTINGS_MODULE=kustosz.settings
export KUSTOSZ_BASE_DIR="$HOME/kustosz_home"
```

At this stage, do all the other setup that your Kustosz installation might require - create (sub)domain, create Postgres user and database, install Redis server and ensure it starts automatically etc. The exact actions to take depend on your operating system and preferred configuration.

## Install Kustosz server

The very first step is creating and activating virtual environment. It must exists as long as you run Kustosz, so you must create it in a path that won't disappear automatically.

You might need to re-create virtual environment once your system Python is upgraded.

It's fine to remove virtual environment and create new one when you upgrade Kustosz to newer version.

```bash
python3 -m venv ~/.virtualenvs/kustosz/
source ~/.virtualenvs/kustosz/bin/activate
```

:::{admonition} Activating virtual environment with environment variables
:class: note

Instead of sourcing activation script, you may also set two environment variables:

```bash
export VIRTUAL_ENV="$HOME/.virtualenvs/kustosz"
export PATH="$VIRTUAL_ENV/bin:$PATH"
```
:::

Once virtual environment is created and activated, you can install Kustosz package:

```bash
pip install --upgrade pip wheel
pip install kustosz
```

## Install additional packages

redis, postgres driver etc.

## Download frontend files

Kustosz server provides REST API only. To make use of it, you also need frontend files that will be sent to browser.

Create new directory on your server. Then open [Kustosz UI releases](https://github.com/KustoszApp/web-ui/releases) page in your browser and find `kustosz.tar.xz` file provided by the newest release. Download that file into created directory and unpack it. You can remove archive afterwards.

```bash
mkdir ~/kustosz_frontend
cd ~/kustosz_frontend
curl https://github.com/KustoszApp/web-ui/releases/download/VERSION_CHANGE/kustosz.tar.xz -o kustosz.tar.xz  # change VERSION_CHANGE to latest version number
tar xf kustosz.tar.xz
rm kustosz.tar.xz
```

## Configure Kustosz

The main configuration file is `$KUSTOSZ_BASE_DIR/settings/settings.yaml`. You can download sample file from git repository.

```
mkdir -p $KUSTOSZ_BASE_DIR/settings/
curl https://raw.githubusercontent.com/KustoszApp/server/main/settings/settings.yaml -o $KUSTOSZ_BASE_DIR/settings/settings.yaml
```

You can modify sample file, or put site-specific modifications in `$KUSTOSZ_BASE_DIR/settings/settings.local.yaml`.

The exact extent of changes is highly dependant on your preferred configuration. Make sure to also read [backend configuration page](../configuration/backend).

Below is non-exhaustive list of settings you might want to change. Consult [Kustosz](../configuration/backend), [Django](https://docs.djangoproject.com/en/stable/ref/settings/) and [Celery](https://docs.celeryq.dev/en/stable/userguide/configuration.html) settings documentation for meaning of specific options.

* `SECRET_KEY` should be set to new value
* `DATABASES`, especially if you want to use PostgreSQL
* `CACHES`, if you want to use Memcached or Redis to store cache
* `ALLOWED_HOSTS` should contain fully qualified domain name where Kustosz is running
* `CORS_ALLOWED_ORIGINS`, if you decide to run frontend and backend on separate domains, this should contain origin of frontend page
* `CELERY_BROKER_URL`, if you decide to use Redis as Celery broker
* `STATIC_ROOT`, if you decide to serve static files using gunicorn; this is path to directory where files are saved, it should be inside `$KUSTOSZ_BASE_DIR`
* `STATICFILES_DIRS`, if you decide to serve static files using gunicorn; this is list of paths of static files to copy, it should contain directory where you extracted frontend files

:::{admonition} Example configuration
:class: note

Settings below assume that you serve Kustosz from `kustosz.example.com`, use PostgreSQL as database and Redis as Celery transport.

```yaml
production:
  DATABASES:
    default:
      ENGINE: 'django.db.backends.postgresql_psycopg2'
      NAME: "kustoszdb"
      USER: "postgres"
      PASSWORD: "postgres_user_password"
      HOST: "localhost"
      PORT: "5432"
  CELERY_BROKER_URL: "redis://localhost:6379/"
  ALLOWED_HOSTS:
    - 'kustosz.example.com'
  STATIC_ROOT: '/home/USER/kustosz_home/frontend_assets'
  STATICFILES_DIRS:
    - '/home/USER/kustosz_frontend'

```
:::

## Run migrations

Migrations change database structure. You have to run migrations before you first start Kustosz, and each time after upgrading to new version.

```bash
kustosz-manager migrate
```

## Create cache tables

This creates database table for cache. You need to run this only once, before you first start Kustosz. You don't have to run it if you use Memcached or Redis for cache.

```bash
kustosz-manager createcachetable
```

## Ensuring Celery is running

Main celery process must be running:

```bash
celery -A kustosz worker -l INFO -Q fetch_channels_content,celery
```

## (Optionally) Set up periodic channel update

Most of the time, you want channel update process to run periodically. Otherwise you won't see new content in your reader.

If you can afford to run another celery process, the best way is to ensure celery beat is running (this is in addition to main celery process):

```bash
celery -A kustosz beat -l INFO
```

Kustosz comes with appropriate celery beat tasks pre-installed, so no further configuration is needed.

Another option is using system scheduler, like cron. Just ensure following command is run every five minutes or so:

```bash
kustosz-manager fetch_new_content --wait
```

## Run collectstatic

## Run gunicorn

```bash
gunicorn kustosz.wsgi --bind 0.0.0.0:8000
```

## Set up WSGI-compatible server in front of gunicorn


`/etc/nginx/sites-enabled/kustosz`



```
upstream kustosz {
    server localhost:8000;
}

server {

    listen 80;

    location / {
        proxy_pass http://kustosz;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
        client_max_body_size 100M;
    }

    location /ui/ {
        alias /home/kustosz/kustosz_front/;
    }

}
```

```bash
systemctl restart nginx
```

## Optional: Install kustosz-node-readability

```bash
npm install -g kustosz-node-readability
```
