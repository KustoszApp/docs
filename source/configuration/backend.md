# Backend

Kustosz uses central configuration storage to maintain configuration for both Kustosz itself and all of the dependencies (Django, Celery etc.). Such central configuration is possible thanks to excellent [Dynaconf](https://www.dynaconf.com/) library. This page covers everything that you need to know to configure Kustosz, but you might want to take a look at Dynaconf documentation, too.

## Configuration sources

Kustosz will read settings from configuration files and environment variables. Environment variables override settings from files.

### Local files

The main configuration file is `$KUSTOSZ_BASE_DIR/settings/settings.yaml`. You have created this file during installation. This file is already present in container image as `/opt/kustosz/web/settings/settings.yaml`.

When `$KUSTOSZ_BASE_DIR` variable is not set, it will default to parent directory of [`settings.py`](https://github.com/KustoszApp/server/blob/main/kustosz/settings.py) file. In production deployments, that's usually `lib/python3.x/site-packages/` directory inside current virtual environment. In development environment, that's root of git tree.

Site-specific modifications can be put in `$KUSTOSZ_BASE_DIR/settings/settings.local.yaml` file. This file will be merged with main configuration file, i.e. any setting not specified in site-specific file will be read from main file. This allows you to copy newest Kustosz configuration file during upgrades without worrying about overwriting your local changes.

Main configuration file has two top-level keys: `default` and `production`. These are called "layered environments". You can switch between environments by setting `ENV_FOR_DYNACONF` variable prior to starting Kustosz. Selected environment is merged with `default` environment, i.e. any setting not specified in `production` environment will be read from `default`.

:::{admonition} Site-specific modifications and layered environments
:class: warning

Layered environments are effectively applied **after** site-specific modifications. Consider these two files:

```{code-block} yaml
:caption: settings.yaml

default:
    STATIC_ROOT: "./static/"

production:
    STATIC_ROOT: "/opt/kustosz/web/static/"
```

```{code-block} yaml
:caption: settings.local.yaml

default:
    STATIC_ROOT: "/home/kustosz/website/static_files/"
```

Assuming `ENV_FOR_DYNACONF=production`, value of `STATIC_ROOT` setting will be **`/opt/kustosz/web/static/`**. That's because `settings.local.yaml` overrides `settings.yaml`, but `production` overrides `default`.

When using layered environments, it is recommended that site-specific configuration file work only on `production` environment.
:::

:::{admonition} Overriding single value in nested structure
:class: note

Django uses complex (hierarchical, nested) structures for some of their settings. If you only want to change single value in hierarchy, double underscore can be used to express "one level down".

Assuming `ENV_FOR_DYNACONF=production`, following file:

```{code-block} yaml
default:
    DATABASES:
      default:
        ENGINE: 'django.db.backends.sqlite3'
        NAME: 'db.sqlite3'

production:
    DATABASES__default__NAME: "/tmp/kustosz.db"
```

would be the same as:

```{code-block} yaml
:emphasize-lines: 5

production:
    DATABASES:
      default:
        ENGINE: 'django.db.backends.sqlite3'
        NAME: '/tmp/kustosz.db'
```

You can use this method to add new keys to nested structure. This new key itself can also be complex, containing other nested items.
:::


### Environment variables

Environment variables should be the same as setting names, but prefixed with `DYNACONF_`. For example, if you want to change value of setting `KUSTOSZ_LOCK_EXPIRE`, then environment variable should be `DYNACONF_KUSTOSZ_LOCK_EXPIRE`.

Environment variables do not support site-specific settings or layered environments. They are simple source of data that overrides everything else.

It is possible to use environment variables to override only one value in complex (hierarchical, nested) structure with the help of double underscores. This works the same as in files.

:::{admonition} Using environment variables to override single value in nested structure
:class: note

Consider following `settings.yaml` file:

```{code-block} yaml
default:
    DATABASES:
      default:
        ENGINE: 'django.db.backends.sqlite3'
        NAME: 'db.sqlite3'
```

If you want to change path where database file will be stored (while still using sqlite3 engine), you can do so with following environment variable:

```
export DYNACONF_DATABASES__default__NAME="/home/kustosz/data/sqlite.db"
```
:::

Environment variable values are assumed to be in [TOML](https://toml.io/en/). It means that boolean, numbers and dates will be cast to their proper type by default. It's easy to specify lists or key-value pairs. You can also force specific type with `@type` syntax. Complex structures can be specified in [JSON](https://www.json.org/). See [Dynaconf documentation on environment variables](https://www.dynaconf.com/envvars/) for some examples.

## Verifying current configuration

With site-specific file overrides, layered environments and environment variables, it might be hard to determine what value will be used. You can use `dynaconf list` command to see all settings and their values.

Before using the command, make sure that `DJANGO_SETTINGS_MODULE` and `ENV_FOR_DYNACONF` variables are set.

```bash
export DJANGO_SETTINGS_MODULE=kustosz.settings
export ENV_FOR_DYNACONF=production
dynaconf list
```

## Available settings

### `KUSTOSZ_DEDUPLICATE_DAYS`

Number of past days to consider when checking if new entry is a duplicate. Increasing this number will make deduplication slower, but makes it less likely that you see duplicates on your main list.

Setting this to `0` will disable deduplication altogether.

See also [Deduplication documentation](basic-usage.md#deduplication).

### `KUSTOSZ_READABILITY_NODE_ENABLED`

Should Kustosz use [kustosz-node-readability](https://www.npmjs.com/package/kustosz-node-readability) to obtain full content of new articles.

kustosz-node-readability uses [Readability.js](https://github.com/mozilla/readability), which is used for Firefox Reader View and by [Pocket](https://getpocket.com/). It's probably the best maintained readability implementation around, but it requires Node.js.

### `KUSTOSZ_READABILITY_NODE_EXECUTABLE`

String with name of kustosz-node-readability executable.

This may be a list of strings, which might be useful if you don't have kustosz-node-readability in your `$PATH`, but you still meet all the other requirements to run it.

This is ignored if `KUSTOSZ_READABILITY_NODE_ENABLED` is False.

### `KUSTOSZ_READABILITY_PYTHON_ENABLED`

Should Kustosz use [python-readability](https://github.com/buriy/python-readability) to obtain full content of new articles.

python-readability is smaller project than Readability.js, and it may miss some content that JavaScript implementation can handle. But it's written in pure Python, so you can surely run it if you can run Kustosz.

### `KUSTOSZ_READING_SPEED_WPM`

Number of words you read per minute. Used when calculating estimated reading time for entries.

Estimated reading time is calculated once and stored in database, so changing this setting will not affect existing articles.

### `KUSTOSZ_PERIODIC_FETCH_NEW_CONTENT_INTERVAL`

How often should Kustosz check for new content of feeds, in minutes.

This value is used only once, during initial database migration. Changing this setting later doesn't affect anything, as value is stored in database.

This value takes effect only if you maintain celery beat process. It is ignored if you start periodic updates through operating system task scheduler.

### `KUSTOSZ_REQUESTS_CACHE_INIT_OPTIONS`

Mapping of key-value pairs passed verbatim to [`requests_cache.session.CachedSession()`](https://requests-cache.readthedocs.io/en/stable/session.html#requests_cache.session.CachedSession). Main use case is specifying path to directory where cache will be stored.

requests_cache is used when downloading HTML pages, which happens for entries added manually and content extracted with readability, assuming at least one of `KUSTOSZ_READABILITY_*_ENABLED` settings is set to True.

### `KUSTOSZ_FEED_READER_WORKERS`

Number of threads to use when getting the feeds. Passed verbatim to [`reader.Reader.update_feeds()`](https://reader.readthedocs.io/en/stable/api.html#reader.Reader.update_feeds).

### `KUSTOSZ_FETCH_CHANNELS_CHUNK_SIZE`

Number of channels to update at once. You might want to lower this setting if your server has limited memory.

### `KUSTOSZ_FETCH_PAGE_MAX_RETRIES`

Number of times to try to download HTML page before giving up. This affects entries added manually and content extracted with readability, assuming at least one of `KUSTOSZ_READABILITY_*_ENABLED` settings is set to True.

### `KUSTOSZ_LOCK_EXPIRE`

When should internal locks expire. You might need to increase this number if you increased `KUSTOSZ_FETCH_CHANNELS_CHUNK_SIZE` or your server is particularly slow.


## Django settings

Kustosz is built with Django, so all Kustosz settings are also Django settings. In fact, Kustosz settings are just special cases of general Django settings.

All Django settings are documented in [Django documentation on Settings](https://docs.djangoproject.com/en/stable/ref/settings/). They cover things like database connection, caching engine, local paths etc. You can use Django settings in `settings.yaml` as-is, with only exception being that Django uses pure Python and Kustosz uses YAML.

## Celery settings

If you want to change Celery configuration, you need to make setting name all-uppercase and prefix it with `CELERY_`. For example, to change Celery setting `broker_url`, use Kustosz configuration variable `CELERY_BROKER_URL`.

All Celery settings are documented in [Celery documentation on Settings](https://docs.celeryq.dev/en/stable/userguide/configuration.html).

:::{admonition} Using environment variables to change Celery settings
:class: note

Changing Celery settings by using environment variables is possible, but note about prefixing setting names still applies. To change Celery setting `broker_url`, set environment variable `DYNACONF_CELERY_BROKER_URL`.
:::
