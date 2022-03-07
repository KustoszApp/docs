# Containers

There is one image, available at [`quay.io/kustosz/app`](https://quay.io/repository/kustosz/app?tab=info). Image is OCI/runc-compatible, meaning it works with [Docker](https://www.docker.com/) and [Podman](https://podman.io/).

## Single container

Kustosz requires background processes, and running multiple processes in single container is generally discouraged. However, it has the benefit of being extremely easy to do.

If you decide to run your main instance in single container, then you should at least use volume or bind mount to store `/opt/kustosz/web/db/` directory content on local host. This way Kustosz database will survive container restart.

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

## docker-compose

## podman pods

## Changing Kustosz configuration

## Container-specific configuration options

There are few environmental variables recognized by container image entry point script, listed below.

None of them is set by default. Setting variable to any non-empty value will cause effect described below variable name. Note that this includes values often considered "falsy", such as number 0, string "false", or string "off". Set variable if you want effect described below, omit it completely to retain default behavior.

You can set variable using `-e` / `--env` flag. If you want to set multiple variables (possibly because you are also changing Kustosz configuration), consider storing them in file and using `--env-file` flag.

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

### `KUSTOSZ_SKIP_MIGRATE`

Migrations change database structure. Kustosz will automatically detect migrations that were run previously on connected database to ensure they are not run again. In other words, it's safe to run migrations multiple times on the same database. However, running them will add some time to container startup.

If you decide to skip migrations in day-to-day operations, there are still two situations when you are required to run them:

* when starting application with new database for the first time, so database can be populated with initial tables structure
* after upgrading Kustosz to newer version, when specific version is run for the first time.

### `KUSTOSZ_SKIP_CREATECACHETABLE`

By default, Kustosz will store cache in main database. In order to do that, additional table must be created. Kustosz will automatically detect when required table is available, so it's safe to call this function multiple times. However, running it will add some time to container startup.

This option is only required when starting application with new database for the first time.

Kustosz supports all [cache backends supported by Django](https://docs.djangoproject.com/en/dev/topics/cache/), except local-memory. If you decide to use memcached as cache backend, there's no need to create cache table, and setting this variable is safe.

### `KUSTOSZ_SKIP_COLLECTSTATIC`

Django, which Kustosz is built upon, requires us to run [`collectstatic`](https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#collectstatic) command during deployment. It will populate special local directory (`/opt/kustosz/web/static/`) with copy of all static files. That copy is considered disposable and can be re-populated every time application is started. However, this re-population will add some time to container startup.

You can skip running `collectstatic` if you decide to store `/opt/kustosz/web/static/` outside of container, so this directory content may survive container restart. When you do that, there are still two situations when you are required to run `collectstatic`:

* when starting application with empty `/opt/kustosz/web/static/` directory for the first time
* after upgrading Kustosz to newer version, when specific version is run for the first time.
