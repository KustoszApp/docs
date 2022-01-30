# Initial setup

After installing application, there are few more things that you need to do before you can use it:

:::{contents}
:class: this-will-duplicate-information-and-it-is-still-useful-here
:::

## Creating new user

    python manage.py createsuperuser --username <user> --email <doesnt@matter.invalid>

## Ensuring Celery is running

Main celery process must be running:

    celery -A kustosz worker -l INFO -Q fetch_channels_content,celery

## Importing OPML with feeds

If you have file in OPML format with list of your subscribed feeds, you can import it using following command:

    python manage.py import_channels --file <path/to/file.xml> opml

## (Optionally) Set up periodic channel update

Most of the time, you want channel update process to run periodically. Otherwise you won't see new content in your reader.

If you can afford to run another celery process, the best way is to ensure celery beat is running (this is in addition to main celery process):

    celery -A kustosz beat -l INFO

Kustosz comes with appropriate celery beat tasks pre-installed, so no further configuration is needed.

Another option is using system scheduler, like cron. Just ensure following command is run every five minutes or so:

    python manage.py fetch_new_content --wait
