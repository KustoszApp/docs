# Initial setup

Kustosz is running and accessible, but it doesn't have any data. You need to create new account to log in the web interface. We recommend that you also import feed data from OPML file and set new value of `SECRET_KEY` setting.

Instructions provided below should be done only once, after initial installation of Kustosz. You don't need to repeat them after upgrading to newer version.

## Creating new user

Kustosz supports only single user, and you need to create it to access the application. This can be done with following command:

    kustosz-manager createsuperuser --email doesnt@matter.invalid

Program will ask for desired username and password. Username can be any string, but you will need to provide it every time you log in, so you might opt in to something that is easy to type.

Each user has to have email address - this is requirement imposed on us by Django, one of Kustosz dependencies. Kustosz never uses your email address and doesn't mind if you provide non-existing address.

## Importing OPML file

Most feed readers have an option to export list of subscribed channels into OPML file. If you have such file, you can import it in Kustosz with following command:

    kustosz-manager import_channels --file <path/to/file.xml> opml

Importing OPML file can take some time, depending on number of channels and amount of content they have published.

You can use above command at any time after installing Kustosz. If OPML file contains reference to feed that you have added earlier, Kustosz will automatically skip it.

## Setting new value of `SECRET_KEY`

`SECRET_KEY` is [Django setting](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-SECRET_KEY) used for various security-related purposes. Your Kustosz installation should have unique `SECRET_KEY` value.

You can set new value any time you want, but you will have to log in again on all your devices.

Obtain new value by running:

```
kustosz-manager generate_secret_key
```

Then, depending on your environment, put it in your `settings.yaml` file or provide as environment variable named `DYNACONF_SECRET_KEY`.
