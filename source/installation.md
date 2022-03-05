# Installation

The easiest way to install Kustosz is by using [containers (Docker, podman)](./installation/containers):

```
docker run quay.io/kustosz/app
```

For production deployments, we recommend using container orchestration tool, such as docker-compose.

Apart from [containers](./installation/containers), we also have instructions for [Heroku](./installation/heroku), [Azure](./installation/azure), [Kubernetes](./installation/kubernetes) and [custom server](./installation/vps) (Raspberry Pi, DigitalOcean Droplets, VPS and shared hosting accounts).

## Installation instructions for software developers

Kustosz is Django application. It requires Python 3.9 or newer and works on Django 3.2 and newer. Data is stored in database engine supported by [Django ORM](https://docs.djangoproject.com/en/dev/ref/databases/). Default setup uses filesystem-backed SQLite, but we recommend PostgreSQL.

Kustosz requires [Celery](https://docs.celeryproject.org/en/stable/) process to handle background tasks. Celery requires transport and backend. We use file system as default transport, but we recommend Redis. We use Django database as default backend.

You have to trigger channel update process periodically. We provide ready-to-use Celery Beat configuration, but it requires starting and maintaining additional Celery process. If you don't like this, you can use OS scheduler, such as cron or systemd. You can find sample configuration files in `./etc/`.

If you are unsure about any of the above, you can find detailed instructions on [custom server](./installation/vps) page.

:::{toctree}
:maxdepth: 1
:hidden:

installation/azure
installation/containers
installation/heroku
installation/kubernetes
installation/vps

:::
