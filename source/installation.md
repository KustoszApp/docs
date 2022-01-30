# Installation

The easiest way to install Kustosz is using [containers (Docker, podman)](). We provide two different images: all-in-one image that contains everything that you need, and set of modular images, where each one provides one piece of entire stack. Set of images is recommended for production usage, but it requires container orchestration tool, such as docker-compose.

Apart from [containers](), we also have instructions for [Heroku](), [Azure](), [Kubernetes]() and [custom server](). Last one is appropriate for VPS, Raspberry Pi and DigitalOcean Droplets.

## Installation instructions for software developers

Kustosz is Django application. It requires Python 3.9 or newer and works on Django 3.2 and newer. Data is stored in database engine supported by [Django ORM](). Default setup uses SQLite, but we recommend PostgreSQL.

Kustosz requires [Celery]() process to handle background tasks. Celery requires transport and backend. We use file system as default transport, but we recommend Redis. We use Django database as default backend.

You have to trigger channel update process periodically. We provide ready-to-use Celery Beat configuration, but it requires starting and maintaining another Celery process. If you don't like this, you can use OS scheduler, such as cron or systemd. You can find sample configuration files in `./etc/`.

If you are unsure about any of the above, you can find detailed instructions on [custom server]() page.
