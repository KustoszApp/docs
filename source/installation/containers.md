# Containers

There is one image, available at [`quay.io/kustosz/app`](https://quay.io/repository/kustosz/app?tab=info). Image is OCI/runc-compatible, meaning it works with [Docker](https://www.docker.com/) and [Podman](https://podman.io/).

## Single container

Kustosz requires background processes, and running multiple processes in single container is generally discouraged. However, it has the benefit of being extremely easy to do.

If you decide to run your main instance in single container, then you should at least use volume or bind mount to store `/opt/kustosz/web/db/` directory content on local host. This way Kustosz database will survive container restart.

Container image will bind Kustosz to port 8000 inside the container. When starting it, you need to bind it to some port on the host machine. Otherwise, Kustosz will not be available.

::::{tab-set}

:::{tab-item} docker
```
docker run -p 127.0.0.1:8000:8000 -v kustosz_db:/opt/kustosz/web/db/ quay.io/kustosz/app
```
:::

:::{tab-item} podman
```
podman run -p 127.0.0.1:8000:8000 -v kustosz_db:/opt/kustosz/web/db/ quay.io/kustosz/app
```
:::

::::

Now proceed to [initial setup](../initial-setup). You can use `docker exec` to execute a command in a context of running container. Kustosz web UI will be available at [localhost:8000/ui/](http://localhost:8000/ui/).

## docker-compose

docker-compose is default container orchestrating tool for Docker. It allows you to manage multiple containers as a single unit.

First, download [docker-compose.yaml](https://github.com/KustoszApp/server/blob/main/containers/docker-compose.yaml) file. Then review it and modify to your liking. You should at least change Postgres password (make sure that you changed all references to old password in the file). Finally, run it:

```
docker-compose -p kustosz -f ./docker-compose.yaml up
```

Now proceed to [initial setup](../initial-setup). You can use `docker exec` to execute a command in a context of running container. Kustosz web UI will be available at [localhost/ui/](http://localhost/ui/).

In default configuration, docker-compose will listen to port 80 on the host machine. If this port is already taken - which is very likely if you have multiple web-based services running - change definition of `ports` in `kustosz_api` container.

docker-compose will start containers for Postgres (database) and Redis (Celery transport). They are commonly used by modern applications and it's possible that you already have them running, or have different images for them. In that case, feel free to change image references or remove them from your `docker-compose.yaml` file. Make sure that applications running in containers can access these external services.

You can switch Redis to any [message broker supported by Celery](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html). RabbitMQ is popular and well-tested option, but it requires more resources.

When using different database or Celery transport, make sure that you also change environment variables telling Kustosz how to connect with these services. These variables start with `DYNACONF_DATABASES__` and `DYNACONF_CELERY_`. Make sure that you change their values in all containers running from `kustosz` image.

## podman pods

podman pods allow multiple containers to share single namespace. This way they can easily access each other, and you can manage them as a single unit.

Pods has seen very active development in Podman 2.x line. We recommend that you use at least Podman 3.0, released in February 2021.

First, download [kustosz_pod.yaml](https://github.com/KustoszApp/server/blob/main/containers/kustosz_pod.yaml) file. Then review it and modify to your liking. You should at least change Postgres password (make sure that you changed all references to old password in the file). Finally, run it:

```
podman play kube ./kustosz_pod.yaml
```

Now proceed to [initial setup](../initial-setup). You can use `podman exec` to execute a command in a context of running container. Kustosz web UI will be available at [localhost/ui/](http://localhost/ui/).

In default configuration, podman will listen to port 80 on the host machine. Usually user processes can't bind to this port. If you want to run rootless podman, you need to change the port in pod definition or change the configuration of host machine. If port 80 is already taken - which is very likely if you have multiple web-based services running - change definition of `ports` in `kustosz_api` container.

podman will start containers for Postgres (database) and Redis (Celery transport). They are commonly used by modern applications and it's possible that you already have them running, or have different images for them. In that case, feel free to change image references or remove them from your `kustosz_pod.yaml` file. Make sure that applications running in containers can access these external services.

You can switch Redis to any [message broker supported by Celery](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html). RabbitMQ is popular and well-tested option, but it requires more resources.

When using different database or Celery transport, make sure that you also change environment variables telling Kustosz how to connect with these services. These variables start with `DYNACONF_DATABASES__` and `DYNACONF_CELERY_`. Make sure that you change their values in all containers running from `kustosz` image.

## Changing Kustosz configuration

All Kustosz configuration options are documented on [backend configuration page](../configuration/backend).

The recommended way of changing configuration of Kustosz running in container is by environment variables. Remember that environment variables must be prefixed by `DYNACONF_` - e.g. to change value of setting `KUSTOSZ_READING_SPEED_WPM`, your environment variable should be named `DYNACONF_KUSTOSZ_READING_SPEED_WPM`.

You can set variable using `-e` / `--env` flag. If you want to set multiple variables, consider storing them in file and using `--env-file` flag.

::::{tab-set}

:::{tab-item} docker

```
docker run -e KUSTOSZ_SKIP_MIGRATE=1 quay.io/kustosz/app
```
```
echo 'KUSTOSZ_SKIP_MIGRATE=1' > production.env
docker run --env-file production.env quay.io/kustosz/app
```
:::

:::{tab-item} podman
```
podman run -e KUSTOSZ_SKIP_MIGRATE=1 quay.io/kustosz/app
```
```
echo 'KUSTOSZ_SKIP_MIGRATE=1' > production.env
podman run --env-file production.env quay.io/kustosz/app
```
:::

::::

Alternatively, you can put `settings.yaml` file in `/opt/kustosz/web/settings` directory inside the container. It is recommended that you store `settings.yaml` file on your host machine and use volume or bind mount to make it accessible inside the container. As this is the only directory where setting files reside, it's best to start with copy of [`settings.yaml` file from Kustosz backend repository](https://github.com/KustoszApp/server/blob/main/settings/settings.yaml).

## Container-specific configuration options

There are few environmental variables recognized by container image entry point script, listed below.

None of them is set by default. Setting variable to any non-empty value will cause effect described below variable name. Note that this includes values often considered "falsy", such as number 0, string "false", or string "off". Set variable if you want effect described below, omit it completely to retain default behavior.

See [](#changing-kustosz-configuration) section above for quick overview of passing environment variables to containers.

### `KUSTOSZ_SKIP_MIGRATE`

Migrations change database structure. Kustosz will automatically detect migrations that were run previously on connected database to ensure they are not run again. In other words, it's safe to run migrations multiple times on the same database. However, running them will add some time to container startup.

If you decide to skip migrations in day-to-day operations, there are still two situations when you are required to run them:

* when starting application with new database for the first time, so database can be populated with initial tables structure
* after upgrading Kustosz to newer version, when specific version is run for the first time.

### `KUSTOSZ_SKIP_CREATECACHETABLE`

By default, Kustosz will store cache in main database. In order to do that, additional table must be created. Kustosz will automatically detect when required table is available, so it's safe to call this function multiple times. However, running it will add some time to container startup.

This option is only required when starting application with new database for the first time.

Kustosz supports all [cache backends supported by Django](https://docs.djangoproject.com/en/stable/topics/cache/), except local-memory. If you decide to use memcached as cache backend, there's no need to create cache table, and setting this variable is safe.

### `KUSTOSZ_SKIP_COLLECTSTATIC`

Django, which Kustosz is built upon, requires us to run [`collectstatic`](https://docs.djangoproject.com/en/stable/ref/contrib/staticfiles/#collectstatic) command during deployment. It will populate special local directory (`/opt/kustosz/web/static/`) with copy of all static files. That copy is considered disposable and can be re-populated every time application is started. However, this re-population will add some time to container startup.

You can skip running `collectstatic` if you decide to store `/opt/kustosz/web/static/` outside of container, so this directory content may survive container restart. When you do that, there are still two situations when you are required to run `collectstatic`:

* when starting application with empty `/opt/kustosz/web/static/` directory for the first time
* after upgrading Kustosz to newer version, when specific version is run for the first time.
