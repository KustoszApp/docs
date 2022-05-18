# Installation

:::{toctree}
:maxdepth: 1
:hidden:
:glob:

installation/*
:::


## Trying it out

There are many ways to install Kustosz, depending on your environment and hosting provider. If you just want to try it out and see if Kustosz is for you, the easiest way is by using containers. Just run:

::::{tab-set}

:::{tab-item} docker
```
docker run -p 127.0.0.1:8000:8000 quay.io/kustosz/app
```
:::

:::{tab-item} podman
```
podman run -p 127.0.0.1:8000:8000 quay.io/kustosz/app
```
:::

::::

Open [localhost:8000/ui/](http://localhost:8000/ui/) in your web browser to access Kustosz. To log in, use credentials printed in container log after "Generated random login credentials" line.

## Production deployments

While you can use above command to start and run your main instance of Kustosz, in production environments we recommend using container orchestration tool, such as docker-compose. We have installation instruction pages for few common deployment targets:

* [Containers](./installation/containers) - docker and podman, including docker-compose and podman pods
* [Heroku](./installation/heroku) (Work In Progress)
* [Azure](./installation/azure) (Work In Progress)
* [Kubernetes](./installation/kubernetes) (Work In Progress)
* [Your own server](./installation/vps) - including Raspberry Pi, DigitalOcean Droplets, VPS, virtual machines and shared hosting accounts

## Quick overview for software developers

If you are software developer and you don't want to plow through detailed instructions, here's a quick summary.

Kustosz is Django application. It requires Python 3.9 or newer and works on Django 3.2 and newer. Data is stored in database engine supported by Django ORM. Default setup uses filesystem-backed SQLite, but we recommend PostgreSQL.

Kustosz requires Celery process to handle background tasks. Celery requires transport and backend. We use file system as default transport, but we recommend Redis. We use Django database as default backend.

You have to trigger channel update process periodically. We provide ready-to-use Celery Beat configuration, but it requires starting and maintaining additional Celery process. If you don't like this, you can use OS scheduler, such as cron or systemd.

If you are unsure about any of the above, you can find detailed instructions on [custom server](./installation/vps) page.
