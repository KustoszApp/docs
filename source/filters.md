# Filters

Filters do something with entries matching criteria. Filters act on entries as they come in.

## Filtering criteria

At the moment, filtering criteria must be input manually. Criteria field works exactly the same as [Advanced searching](./searching.md#advanced-search) field. You can use the same fields and lookup methods, and you can compose them into advanced queries using ampersand.

## Actions

Each action works on a single matching entry. If there are multiple matching entries, action will be run this many times.

### Mark as read

Automatically marks matched entry as read. It will be stored in Kustosz, but you won't see it in main entries list by default.

This is especially useful for feed aggregators (planets) and larger sites that have multiple authors (perhaps you don't fancy some of them). If you want to hide all entries from specific channel, consider [deactivating the channel](./basic-usage.md#deactivating-a-channel).

### Assign tag

Add a **single** tag to matching entry. This action requires an argument, which is a tag name. Tag will be created when assigned for the first time, if it does not exist.

### Run external application

Run external application (script) on matching entry. This action requires an argument, which is a path to executable. We recommend using absolute paths.

Application will be run only once. If you want to handle expected failure conditions, do so in your application.

Kustosz expects that external application will finish within 30 seconds. If your action might need more time, your application should be lightweight wrapper that starts the long-running script outside of the main process and returns. In shell, consider using `nohup` or `disown`.

Kustosz will pass a number of information through environmental variables. The full list is below. Note that all environmental variable values are strings - you might need to cast them to integers, booleans or dates in your application.

* `KUSTOSZ_ID` - internal id of entry. Can be used if you want to communicate back with Kustosz using API or `kustosz-manager shell`
* `KUSTOSZ_GID` - id of entry, as claimed by source feed
* `KUSTOSZ_ARCHIVED` - boolean value specifying whether entry is archived (read) or not
* `KUSTOSZ_LINK` - URL of entry, as claimed by source feed
* `KUSTOSZ_TITLE` - title of entry
* `KUSTOSZ_AUTHOR` - author field of entry, as claimed by source feed
* `KUSTOSZ_PUBLISHED_TIME_UPSTREAM` - timestamp when entry was published, as claimed by source feed; many feeds skip this field, and some broken feeds also change it when entry is updated 
* `KUSTOSZ_UPDATED_TIME_UPSTREAM` - timestamp when entry was last updated, as claimed by source feed; most content is never updated, so it is often the same as `KUSTOSZ_PUBLISHED_TIME_UPSTREAM`
* `KUSTOSZ_ADDED_TIME` - timestamp when entry was added to Kustosz database; you almost certainly want to use `KUSTOSZ_PUBLISHED_TIME_UPSTREAM`
* `KUSTOSZ_UPDATED_TIME` - timestamp when entry was last updated in Kustosz database; you almost certainly want to use `KUSTOSZ_UPDATED_TIME_UPSTREAM`
* `KUSTOSZ_TAGS` - comma-separated list of entry tags slugs
* `KUSTOSZ_CHANNEL_ID` - internal id of channel
* `KUSTOSZ_CHANNEL_URL` - URL of channel
* `KUSTOSZ_CHANNEL_CHANNEL_TYPE` - internal value specifying channel type; see [`ChannelTypesEnum`](https://github.com/KustoszApp/server/blob/main/kustosz/enums.py#L4) in server source
* `KUSTOSZ_CHANNEL_DISPLAYED_TITLE` - title of channel, as visible in user interface; `KUSTOSZ_CHANNEL_TITLE` when provided, with automatic fallback to `KUSTOSZ_CHANNEL_TITLE_UPSTREAM`
* `KUSTOSZ_CHANNEL_TITLE` - title of channel, as provided by the user; may be empty and you almost certainly want to use `KUSTOSZ_CHANNEL_DISPLAYED_TITLE`
* `KUSTOSZ_CHANNEL_TITLE_UPSTREAM` - title of channel, as claimed by source feed; you almost certainly want to use `KUSTOSZ_CHANNEL_DISPLAYED_TITLE`
* `KUSTOSZ_CHANNEL_LINK` - URL of channel, as claimed by source feed
* `KUSTOSZ_CHANNEL_LAST_CHECK_TIME` - timestamp when channel was last checked for new content
* `KUSTOSZ_CHANNEL_LAST_SUCCESSFUL_CHECK_TIME` - timestamp when last check for new content was successful
* `KUSTOSZ_CHANNEL_ADDED_TIME` - timestamp when channel was added to Kustosz database
* `KUSTOSZ_CHANNEL_ACTIVE` - boolean value specifying whether channel is active or not
* `KUSTOSZ_CHANNEL_UPDATE_FREQUENCY` - how often channel is checked for new content, in seconds
* `KUSTOSZ_CHANNEL_DEDUPLICATION_ENABLED` - boolean value specifying whether deduplication is enabled for channel or not
* `KUSTOSZ_CHANNEL_TAGS` - comma-separated list of channel tags slugs
