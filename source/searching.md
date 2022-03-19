# Searching

Searching allows to change content displayed on main articles list.

## Basic search

Basic search is displayed by default and allows to use graphical user interface to perform basic queries. Basic search interface is intentionally limitied to few most often used options.

* Unread only button - when this button is selected (which it is by default), archived entries will not be displayed. When it is pressed off, both archived and unarchived entries are displayed.
* Date selector - allows to see only entries published before / after yesterday, 2 days ago, a week ago or 2 weeks ago.
* Tag selector - allows to see entries tagged with specific tag. Multiple tags are alternated (joined with conjunction OR), i.e. if entry is tagged with any of the provided tags, it will be on the results list.

## Advanced search

Advanced search allow to perform much wider range of queries, but they require you to write queries by hand. At the moment, there is no autocompletion support.

Table below contains list of fields and possible lookups. Fields and lookups are separated by double underscore: `field__lookup`. Default lookup method, `exact`, can be skipped. Value for lookup is specified after equals sign: `field=value`. Some lookup methods can take in multiple arguments - they are separated by comma. Multiple query parameters are joined with ampersand: `field1=value&field2=value`. See [](#examples) below.

Lookup semantics are generally the same as in Django. See [Django documentation on field lookups](https://docs.djangoproject.com/en/dev/ref/models/querysets/#field-lookups) for details. Special lookup method `not` is logical negation - it will match everything **except** specified value.

### Fields and lookups

````{list-table}
:header-rows: 1
:width: 100%
:widths: 25 25 50

* - Field
  - Lookup methods
  - Notes
* - `archived`
  - * `exact`
  - Boolean field that takes `true` and `false` as values.
* - `link`
  - * `exact`
    * `iexact`
    * `contains`
    * `icontains`
    * `startswith`
    * `istartswith`
    * `endswith`
    * `iendswith`
  -
* - `title`
  - * `exact`
    * `iexact`
    * `contains`
    * `icontains`
    * `startswith`
    * `istartswith`
    * `endswith`
    * `iendswith`
  -
* - `published_time`
  - * `exact`
    * `lt`
    * `gt`
    * `lte`
    * `gte`
  - Publication time as specified by source feed. It will fall back automatically to last updated time if publication time is not specified by source feed.
* - `published_time_upstream`
  - * `exact`
    * `lt`
    * `gt`
    * `lte`
    * `gte`
  - Publication time as specified by source feed. Many feeds skip this field, and some broken feeds also change it when entry is updated. You almost certainly want to use `published_time` instead.
* - `updated_time_upstream`
  - * `exact`
    * `lt`
    * `gt`
    * `lte`
    * `gte`
  - Last updated time as specified by source feed. Most content is never updated, so it is often the same as `published_time_upstream`. You almost certainly want to use `published_time` instead.
* - `added_time`
  - * `exact`
    * `lt`
    * `gt`
    * `lte`
    * `gte`
  - Time when entry was added to Kustosz database. When you add new channel, all entries will have the same `added_time`. You almost certainly want to use `published_time` instead, or maybe `published_time_upstream`.
* - `updated_time`
  - * `exact`
    * `lt`
    * `gt`
    * `lte`
    * `gte`
  - Time when entry was last updated in Kustosz database. You almost certainly want to use `published_time` instead, or maybe `updated_time_upstream`.
* - `tags`
  - * `exact`
    * `not`
  - May be a list. Refers to tags of **entries**.
* - `has_tags`
  - 
  - Boolean field that takes `true` and `false` as values. Finds entries with any tag or no tag at all.
* - `channel`
  - * `exact`
    * `not`
  - May be a list. Uses internal id of channels.
* - `channel_tags`
  - * `exact`
    * `not`
  - May be a list. Refers to tags of **channels**.
* - `channel_has_tags`
  -
  - Boolean field that takes `true` and `false` as values. Finds entries coming from **channels** with any tag or no tag at all.
````

### Working with tags

Under the hood, tags have names (user-visible strings) and slugs (URL-friendly strings). Slugs are automatically derived from names using [`django.utils.text.slugify()`](https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.text.slugify) function (click the link for description of exact transformations applied). 

As an user, you are mostly dealing with names. However, advanced search expects you to use tag **slugs**. That begs the question: how can you obtain the tag slug?

The easiest way is opening browser development tools and refreshing the page. In "Network" tab, you will see requests to `/api/v1/tags/entry` and `/api/v1/tags/channel` endpoints. Responses of these requests contain the list of all entry and channel tags, respectively. Each item on the list will have both `name` and `slug` property.

Alternatively, you can connect to the host where Kustosz is running and run following command to open development shell:

```
kustosz-manager shell
```

Then, run following commands to get the list of all tags:

```
from kustosz.models import Channel, Entry
[f"{i.name}: {i.slug}" for i in Channel.tags.all()]
[f"{i.name}: {i.slug}" for i in Entry.tags.all()]
```

### Examples

Entries published in a year 2022:

```
published_time__gte=2022-01-01T00:00:00&published_time__lte=2022-12-31T23:59:59
```

Entries with title that contain the word "test", case insensitive:

```
title__icontains=test
```

Entries published in a year 2022 with title that contains the word "test", case insensitive:

```
published_time__gte=2022-01-01T00:00:00&published_time__lte=2022-12-31T23:59:59&title__icontains=test
```

Entries with title that starts with the phrase "The quick brown fox", case sensitive (note space is not escaped or put in quotes):

```
title__startswith=The quick brown fox
```

All entries, except these tagged with tag "slug" or "snail" (this includes entries that are not tagged at all):

```
entry_tags__not=slug,snail
```

Entries coming from three specific channels:

```
channel=5,10,15
```

Entries coming from channels that are not tagged (entries themselves may be tagged):

```
channel_has_tags=false
```
