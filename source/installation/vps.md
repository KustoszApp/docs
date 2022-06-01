# Manual installation

:::{admonition} User attention is required
:class: warning

Kustosz is flexible and supports deployments to various environments. This guide limits a number of choices covered to lower cognitive load and provide instructions that are easier to follow. However, it still **expects you to understand what is happening and adjust specific steps to your particular environment**. It is recommended that you familiarize yourself with entire document before taking any action, including [](#additional-setup-instructions) section.
:::

This page covers manual installation of Kustosz. It's intended for users who require maximum flexibility or want deeper understanding of Kustosz deployments. Majority of users should be able to deploy Kustosz using [automatic installer](./vps-installer).

## Prerequisites

Kustosz is web application. You probably want it available under a dedicated (sub)domain that supports secure HTTPS connection. Configuration of domain, HTTPS and access control is outside of scope of this guide.

There are few dependencies that you absolutely must meet:

* Python 3.9 or newer
* Ability to execute arbitrary commands in the context of server
* Ability to start your own long-running processes (needed by Celery worker)
* At least 256 MiB of memory

While not required, we also recommend:

* [PostgreSQL](https://www.postgresql.org/) database server
* [Redis](https://redis.io/) as Celery transport

## Prepare Kustosz server environment

Create Kustosz base directory. This is where you will put settings, and where Kustosz will store SQLite database file and certain cache files.

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

## (Optional) Install additional Python packages

Depending on your preferred configuration, you might need to install additional Python modules, such as:

* `redis` is required to use Redis for cache or as Celery transport
* `psycopg2` is required to connect to PostgreSQL database (psycopg2 requires [additional system packages to build](https://www.psycopg.org/docs/install.html#build-prerequisites))
* `pylibmc` or `pymemcache` is required to use Memcached for cache
* `whitenoise` may be used to [serve static files directly from WSGI server](#use-gunicorn-to-serve-static-files)

```bash
pip install redis psycopg2
```

## (Optional) Install `kustosz-node-readability`

While syndication formats exists so users can read content in their reader applications, many authors try to force readers to visit the website. Kustosz can automatically extract full article content from source page. This extraction is done by "readability" algorithm.

If you have Node.js on your server, you can install [kustosz-node-readability](https://www.npmjs.com/package/kustosz-node-readability). It uses [Readability.js](https://github.com/mozilla/readability), algorithm implementation used for Firefox Reader View and by [Pocket](https://getpocket.com/). It's probably the best maintained readability implementation around.

```bash
npm install -g kustosz-node-readability
```

## Configure Kustosz

The main configuration file is `$KUSTOSZ_BASE_DIR/settings/settings.yaml`. You can download sample file from git repository.

```
mkdir -p $KUSTOSZ_BASE_DIR/settings/
curl https://raw.githubusercontent.com/KustoszApp/server/main/settings/settings.yaml -o $KUSTOSZ_BASE_DIR/settings/settings.yaml
```

You can modify sample file, or put site-specific modifications in `$KUSTOSZ_BASE_DIR/settings/settings.local.yaml`. Second option is preferred, as it allows you to overwrite `settings.yaml` file during upgrade, while keeping site-specific settings safely separated.

The exact changes to make are highly dependant on your preferred configuration. Make sure to also read [backend configuration page](../configuration/backend).

Below is non-exhaustive list of settings you might want to change. Consult [Kustosz](../configuration/backend), [Django](https://docs.djangoproject.com/en/stable/ref/settings/) and [Celery](https://docs.celeryq.dev/en/stable/userguide/configuration.html) settings documentation for meaning of specific options.

* `SECRET_KEY` should be set to new value, obtained by running `kustosz-manager generate_secret_key`
* `ALLOWED_HOSTS` should contain fully qualified domain name where Kustosz is running
* `DATABASES`, especially if you want to use PostgreSQL
* `CACHES`, if you want to use Memcached or Redis for cache
* `CORS_ALLOWED_ORIGINS`, if you decide to run frontend and backend on separate domains, this should contain [origin](https://developer.mozilla.org/en-US/docs/Glossary/Origin) of frontend page
* `CELERY_BROKER_URL`, if you decide to use Redis as Celery broker
* `KUSTOSZ_READABILITY_NODE_ENABLED`, if you have installed kustosz-node-readability
* `STATIC_ROOT`, if you decide to serve static files using gunicorn; this is path to directory where files will be copied to, it should be inside `$KUSTOSZ_BASE_DIR`
* `STATICFILES_DIRS`, if you decide to serve static files using gunicorn; this is list of paths of static files to copy, it should contain directory where you [extract frontend files](#download-frontend-files)

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

In default configuration, Kustosz uses main database for cache. Database must first be prepared for that. You need to run this only once, before you first start Kustosz. You don't have to run it if you use Memcached or Redis for cache.

```bash
kustosz-manager createcachetable
```

## Start main Celery process

Kustosz requires main Celery process to be running. It is used to handle all background tasks, such as downloading files or running filters.

Command to start Celery process is:

```bash
celery -A kustosz worker -l INFO -Q feed_fetcher,celery
```

Due to way Kustosz is designed, some background tasks should run serially. The best way of ensuring that is by running separate Celery process with single worker for `feed_fetcher` queue. The downside is that it requires more system resources.

```bash
celery -A kustosz worker -l INFO -Q celery
celery -A kustosz worker -l INFO -Q feed_fetcher --concurrency 1
```

It is recommended that you use process supervisor to run commands above. Most Linux systems come with systemd, which may be used for that purpose - see [](#use-systemd-to-ensure-background-processes-are-running). Another option is [Supervisor](http://supervisord.org/) - see [](#use-supervisor-to-ensure-background-processes-are-running).

## Run gunicorn

It's finally time to start main Kustosz server. We install and run [gunicorn](https://gunicorn.org/), but you can use any [WSGI](https://wsgi.readthedocs.io/)-compatible web server. [uWSGI](https://uwsgi-docs.readthedocs.io/) is another popular option. If you use Apache web server, you may want to use [mod_wsgi](https://modwsgi.readthedocs.io/).

```bash
pip install gunicorn
gunicorn kustosz.wsgi --bind 0.0.0.0:8000
```

## Download frontend files

Kustosz server provides REST API only. To make use of it, you also need a client.

Create new directory on your server. Open [Kustosz web UI releases](https://github.com/KustoszApp/web-ui/releases) page in your browser and find `kustosz.tar.xz` file provided by the newest release. Download that file into created directory and unpack it. You can remove archive afterwards.

```bash
mkdir ~/kustosz_frontend
cd ~/kustosz_frontend
curl -L https://github.com/KustoszApp/web-ui/releases/download/VERSION_NUMBER/kustosz.tar.xz -o kustosz.tar.xz  # change VERSION_NUMBER to latest version number
tar xf kustosz.tar.xz
rm kustosz.tar.xz
```

## Set up HTTP proxy in front of gunicorn

Most of dedicated WSGI web servers consider serving static files as out of their scope. Usually it is recommended that you set up HTTP proxy in front of WSGI server. [NGINX](https://www.nginx.com/) is popular web server that is commonly used as such proxy. Most Linux distributions have NGINX package that you can install.

After installing NGINX, create `/etc/nginx/sites-available/kustosz` file with following content:

```{code-block}
:caption: /etc/nginx/sites-available/kustosz
:emphasize-lines: 2,19

upstream kustosz {
    # port number here must be the same as port number in gunicorn --bind command
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
        # this must be absolute path to directory where you extracted frontend files
        alias /home/USER/kustosz_front/;
    }

}
```

Make configuration available to NGINX server and restart it so changes can be applied:

```bash
ln -s /etc/nginx/sites-available/kustosz /etc/nginx/sites-enabled/
systemctl restart nginx
```

:::{admonition} NGINX default configuration and file permissions
:class: note

Single NGINX server can serve multiple websites. If you have just installed NGINX, it's likely that it already serves default "NGINX is working" site. It probably binds to port 80, same as Kustosz. This site is configured in `/etc/nginx/sites-enabled/default` file, and it is safe to remove it.

NGINX often runs as an user with limited permissions, such as `www`, `www-data`, `nginx` or `nobody`. You need to ensure that this user has permissions to read extracted frontend files. It also needs executable bit on all directories in the path.
:::

Congratulations! You should see Kustosz running at <http://your-domain/ui/>.

## Additional setup instructions

Following section documents configuration changes that do not apply to all deployments, but are still common. Some of these instructions extend basic installation described above, while some override parts of it.

### Set up periodic channels update with Celery

As noted in [automatic channels update](../basic-usage.md#automatic-channels-update-frequency) section, Kustosz requires channels update process to run periodically. The preferred way of ensuring this process is run is by using Celery beat. Celery beat must run in the background all the time in addition to main Celery process.

```bash
celery -A kustosz beat -l INFO
```

### Set up periodic channel update with cron

As noted in [automatic channels update](../basic-usage.md#automatic-channels-update-frequency) section, Kustosz requires channels update process to run periodically. If you can't run Celery beat, you may use system scheduler, such as cron.

The command that you want to run is:

```bash
kustosz-manager fetch_new_content --wait
```

To run it with cron, use `crontab -e` command and add the following line:

```
*/5 * * * *  kustosz-manager fetch_new_content --wait
```

cron jobs usually run in special environment that differs from normal shell. Remember that Kustosz command line tools require [few environment variables](#prepare-kustosz-server-environment) and [active virtual environment](#install-kustosz-server). You might want to create simple wrapper script that sets up these variables before running the command. Example of such wrapper is available in source code repository in [`etc/cron/kustosz-fetch-content.sh`](https://github.com/KustoszApp/server/blob/main/etc/cron/kustosz-fetch-content.sh).

### Use systemd to ensure background processes are running

Kustosz requires some background processes to run all the time - main Celery process, Celery beat process (optionally), gunicorn WSGI server (optionally). One way to ensure they are running is [systemd](https://www.freedesktop.org/wiki/Software/systemd/). Unlike supervisor, systemd can start processes automatically during system boot.

Systemd is default init in most of Linux distributions.

Sample systemd unit file is available in source code repository in [`/etc/systemd/system/kustosz@.service`](https://github.com/KustoszApp/server/blob/main/etc/systemd/system/kustosz%40.service). This is unit template that calls dispatcher script to start the actual process. Dispatcher script is responsible for setting [required environment variables](#prepare-kustosz-server-environment) and [activating virtual environment](#install-kustosz-server). Sample dispatcher script is provided in [`/etc/systemd/bin/kustosz-service-dispatcher`](https://github.com/KustoszApp/server/blob/main/etc/systemd/bin/kustosz-service-dispatcher).

Put dispatcher script anywhere on your file system and unit file in `/etc/systemd/system/`. Start and enable all background processes:

```
systemctl enable --now kustosz@worker.service
systemctl enable --now kustosz@feedfetcher.service
systemctl enable --now kustosz@clock.service
systemctl enable --now kustosz@web.service
```

### Use supervisor to ensure background processes are running

Kustosz requires some background processes to run all the time - main Celery process, Celery beat process (optionally), gunicorn WSGI server (optionally). One way to ensure they are running is [supervisor](http://supervisord.org/).

You can install supervisor in your virtual environment with `pip install supervisor`.

Sample supervisor config is available in source code repository in [`etc/supervisor/supervisord.conf`](https://github.com/KustoszApp/server/blob/main/etc/supervisor/supervisord.conf). Feel free to adjust it to your liking and to better fit your environment. Sample config file requires `run` and `logs` directories to exist in the same directory as supervisord.conf file and does not start gunicorn process automatically.

Finally, start supervisor:

```bash
supervisord -c path/to/supervisord.conf
```

supervisor can ensure that certain processes are running, but it has one drawback - you need to start it manually. supervisor documentation has section on [starting supervisord on system startup](http://supervisord.org/running.html#running-supervisord-automatically-on-startup). Some Linux distributions, like Debian, offer supervisor package with init daemon script that can be used to start it automatically. If you go down this path, remember that Kustosz command line tools require [few environment variables](#prepare-kustosz-server-environment) and [active virtual environment](#install-kustosz-server). You might also need to ensure correct file permissions, as supervisor will be running as privileged user, while Kustosz was installed for standard user.

### Use gunicorn to serve static files

[WhiteNoise](http://whitenoise.evans.io/) is project dedicated to making WSGI-compatible web servers better at serving static files. Serving static content is main reason this guide uses NGINX, so with WhiteNoise you might not need NGINX anymore. The second reason is security, so you probably still want *some* kind of HTTP proxy in front of WhiteNoise-enabled WSGI server.

First, install WhiteNoise:

```
pip install whitenoise
```

Configure Kustosz:

* `STATICFILES_DIRS` should contain directory where you [extracted frontend files](#download-frontend-files); this setting is list of paths
* `STATIC_ROOT` should be a path to directory where static files will be copied to; it should be inside `$KUSTOSZ_BASE_DIR`
* `STATICFILES_STORAGE` should be set to `"whitenoise.storage.CompressedManifestStaticFilesStorage"`
* `MIDDLEWARE` should contain `"whitenoise.middleware.WhiteNoiseMiddleware"` as third entry on the list, **below** `"django.middleware.security.SecurityMiddleware"` and `"corsheaders.middleware.CorsMiddleware"`; see [container `settings.local.yaml`](https://github.com/KustoszApp/server/blob/main/containers/settings.local.yaml#L5=) in source code repository
* `STATIC_URL` must be set

Finally, run `collectstatic` command. This command will walk through all directories specified in `STATICFILES_DIRS` and copy files into `STATIC_ROOT`, where they will be processed (i.e. compressed).

```bash
kustosz-manager collectstatic
```

You have to run above command before you first start Kustosz, and each time after upgrading to new version.

% FIXME:
% ### Serve UI and API on different domains
