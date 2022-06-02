# Heroku

Deploying on Heroku is as easy as clicking the button below:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/KustoszApp/kustosz-heroku)

Fill in the form, click "Deploy app" button, wait about a minute and click "View" button. Use username and password provided in Heroku deployment form to log in.

## Deploying manually

If you want to modify your Kustosz instance before deployment, or don't like clicking buttons, you can deploy it manually using [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

First, clone kustosz-heroku repository:

    git clone https://github.com/KustoszApp/kustosz-heroku

Perform any modifications to repository files and commit them. Don't push your changes.

If you would like to import OPML file during deployment, create `kustosz/opml` directory and put XML file there.

Create new Heroku app. You can pass `--region=<region_id>` to deploy to specific region. Use `heroku regions` for list of available regions.

    APP_NAME="my-kustosz-instance-name"
    heroku create --addons=heroku-postgresql:hobby-dev "$APP_NAME"

Set required environment variables:

    heroku config:set ENV_FOR_DYNACONF=production
    heroku config:set DYNACONF_ALLOWED_HOSTS="[\"$APP_NAME.herokuapp.com\"]"

Set username and password. This step is optional and if you don't set these variables, random password will be generated automatically during initial deployment. It will be printed to deployment log, but this is the only time you will see it.

    heroku config:set KUSTOSZ_USERNAME=<username of your choice>
    heroku config:set KUSTOSZ_PASSWORD=<password of your choice>

Add buildpacks explicitly:

    heroku buildpacks:add heroku/nodejs
    heroku buildpacks:add heroku/python

Push current branch to Heroku. This will build new version and deploy it:

    git push heroku main

Finally, set new [Django SECRET_KEY](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-SECRET_KEY). This can't be done automatically during deployment, because resetting this variable will log out all users.

    heroku config:set DYNACONF_SECRET_KEY="$(heroku run kustosz-manager generate_secret_key)"

That's it! Your Kustosz is now available under [$APP_NAME.herokuapp.com/ui/](https://my_heroku_app_name.herokuapp.com/ui/)

## Importing OPML file

Most feed readers have an option to export list of subscribed channels into OPML file. If you have such file, you can import it during Kustosz deployment. Just create `kustosz/opml` directory and put XML file there:

    mkdir kustosz/opml
    cp <path/to/file.xml> kustosz/opml/
    git add kustosz/opml/*.xml
    git commit -m 'Adding OPML file'

Importing OPML file can take some time, depending on number of channels and amount of content they have published. There's no reason to import the same file during every subsequent deployment (e.g. when you update Kustosz to newest version), so once file has been imported, you can tell deployment script to skip this step:

    heroku config:set KUSTOSZ_SKIP_IMPORT_CHANNELS=1

## Considerations when running Kustosz on paid plans

[kustosz-heroku](https://github.com/KustoszApp/kustosz-heroku) repository is designed to use **single dyno** on **free plan**. Kustosz deployed from this repository won't be able to scale horizontally.

The first limit you are likely to encounter is Postgres row limit. Free tier provides only 10 000 rows, which can be quickly exhausted with just 100 feeds. Hobby Basic tier costs 9 USD per month and offers 10 000 000 row limit, which is virtually unlimited as far as Kustosz is concerned.

You also need Redis to allow multiple dynos to coordinate their work. Free Redis tier will not allow enough connections.

    heroku addons:create heroku-redis:premium-1

kustosz-heroku repository comes with sample Procfile for scalable deployments, `Procfile.scalable`. You should use it instead of default `Procfile`:

    mv Procfile.scalable Procfile
    git add Procfile
    git commit -m 'Use scalable Procfile'

Once application is deployed, you need to start dynos for additional process types:

    heroku ps:scale worker=1 clock=1 feedfetcher=1

You should **never** have more than single `clock` and `feedfetcher` processes - the first one is lightweight process responsible for starting recurring background tasks, and second is responsible for processing sequential queues. However, you are free to start multiple `worker` and `web` processes:

    heroku ps:scale web=2 worker=6

## Heroku-specific configuration options

There are few environmental variables recognized by Heroku deployment script, listed below.

None of them is set by default.

Most variables act as flags - script only checks if they have been set, ignoring their value. In these cases, setting variable to any non-empty value will cause effect described below variable name. Note that this includes values often considered "falsy", such as number 0, string "false", or string "off". Set variable if you want effect described below, omit it completely to retain default behavior.

You can set these variables in your application settings in Heroku web dashboard or with Heroku CLI:

    heroku config:set VARIABLE_NAME=<value>


### `KUSTOSZ_USERNAME`

Username that you will use to log in to Kustosz in your browser. If user doesn't exist, it will be created automatically. Password will be set to value of `KUSTOSZ_PASSWORD`, which must also be set.

If omitted, default value of `admin` will be assumed, unless `KUSTOSZ_SKIP_PASSWORD_GENERATION` is also set.

### `KUSTOSZ_PASSWORD`

Password that you will use to log in to Kustosz in your browser.

If omitted, random password will be generated, unless `KUSTOSZ_SKIP_PASSWORD_GENERATION` is also set. Password value will be displayed in container log.

### `KUSTOSZ_SKIP_PASSWORD_GENERATION`

By default, Heroku deployment script will generate random password for `admin` user and print it in log. This password is only used if `admin` user doesn't already exist. Since this is very fast operation, it is generally safe to run it every time you deploy your application.

If `KUSTOSZ_USERNAME` and `KUSTOSZ_PASSWORD` are set, they will be used instead and password will not be generated or displayed in log.

If you set this variable and **don't** set `KUSTOSZ_USERNAME` and `KUSTOSZ_PASSWORD`, no user will be created. If this is your first time deploying Kustosz, you won't be able to log in until you create new user manually.

### `KUSTOSZ_SKIP_IMPORT_CHANNELS`

If you have added OPML file (see [](#importing-opml-file)) and deployed your application, there's no reason to import the same file during each subsequent deployment (e.g. when you update Kustosz to newest version). You can tell deployment script to skip this step by setting this variable.

### `KUSTOSZ_SKIP_MIGRATE`

Migrations change database structure. Kustosz will automatically detect migrations that were run previously on connected database to ensure they are not run again. In other words, it's safe to run migrations multiple times on the same database. However, running them will make deployment a little slower.

If you decide to skip migrations in day-to-day operations, there are still two situations when you are required to run them:

* when starting application with new database for the first time, so database can be populated with initial tables structure
* after upgrading Kustosz to newer version, when specific version is run for the first time.

### `KUSTOSZ_SKIP_CREATECACHETABLE`

By default, Kustosz will store cache in main database. In order to do that, additional table must be created. Kustosz will automatically detect when required table is available, so it's safe to call this function multiple times. However, running them will make deployment a little slower.

This option is only required when deploying Kustosz for the first time.

Kustosz supports all [cache backends supported by Django](https://docs.djangoproject.com/en/stable/topics/cache/), except local-memory. If you decide to use memcached as cache backend, there's no need to create cache table, and setting this variable is safe.
