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

### `KUSTOSZ_SKIP_CREATECACHETABLE`

### `KUSTOSZ_SKIP_COLLECTSTATIC`

