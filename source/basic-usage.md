# Basic usage

Kustosz user interface follows familiar pattern used by many other news reading applications: navigation pane on the left and central list of items on the right. Article below is not exhaustive and documents only features that are specific to Kustosz or might be hard to discover. Two prominent features are documented on separate pages: [](./searching) and [](./filters).

## Keyboard navigation

You can use your keyboard to quickly move through articles:

* `j` - move to next article and open it
* `k` - move to previous article and open it
* `n` - move to next article without opening it (currently opened article will remain open)
* `b`, `p` - move to previous article without opening it (currently opened article will remain open)
* `o`, `Space`, `Enter` - open currently selected article, or close if it's already opened
* `m` - mark currently selected article as read, or mark it back as unread

## Automatic channels update frequency

When editing a channel, you can set automatic update frequency - how often Kustosz should check for new content. Default value is every one hour. If channel is lower priority for you or is known to publish seldom, you can check it less often. If you want to ensure that you learn about new content quickly enough and channel publishes a lot of content, you can check it more frequently.

Every time you check for new content, website server uses a little bit of resources. Some websites might be behind firewall or CDN that will detect too frequent connections and block them, thinking this might be some sort of attack. That's why you should not check for new content *too often*. Every 30 minutes is reasonable lower limit.

Kustosz relies on external scheduler to start channels update procedure - you might have set it up during installation, depending on your deployment environment. We recommend that channels update process is run every 5 minutes. This value puts effective limit on channels update frequency. If you have set up external scheduler to check for updates every hour, and set update frequency of specific channel to 5 minutes, that channel will still be updated every hour.

## Using local file as channel source

Kustosz can read content from any XML file that follows RSS or ATOM specification. While most of these files are delivered through web, you can use local file as well. This way Kustosz can read any content source it does not handle natively - as long as you can transform it into RSS or ATOM file.

First, save XML files inside the `$KUSTOSZ_BASE_DIR/feeds` directory. You can create directories inside to organize your files. Then, run following command:

```
kustosz-manager import_channels --wait autodiscover
```

If you add new files in the future, just re-run the command.

## Deactivating a channel

When modifying a channel, you can toggle "active" flag. When "active" flag is disabled (channel is not active), it will not be checked for new content during channels update. 

Deactivating a channel is intermediate step before removing it. Channel is not checked for new content, but all past content is still available in the application. This is especially useful for channels that disappeared from the web, stopped being updated or are very active and you want to silent them for a while.

## Deduplication

Deduplication automatically marks some entries as read, so they don't appear on the default list of entries when opening the application.

Deduplication is turned on by default. You can opt-out specific channels by turning off "is deduplicated" flag. When flag is disabled, entries from that channel are never marked as read by deduplication algorithm. You can also turn off deduplication altogether by setting `KUSTOSZ_DEDUPLICATE_DAYS` setting to `0`.

Deduplication works only across channels, i.e. entries from one channel are never considered a duplicates. That's because some authors use the same title for all of their posts.

Deduplication algorithm looks into entry GID, normalized link and author-title pair. If any of these values is the same as for one of other entries, latter entry is considered a duplicate. By default, deduplication algorithm looks into all entries added in last 2 days.

## Adding web page manually

You can add any web page to Kustosz. This is especially useful for older articles that no longer appear in website feed, for articles published by websites that don't publish feed, or when you don't want to subscribe to feed.

The easiest way to add specific web page is through following command:

```
kustosz-manager add_entry --link 'http://URL_OF_WEB_PAGE'
```

Alternatively, you can add web page by sending carefully-crafted HTTP request to your Kustosz server. This can be done from any computer, but requires valid authorization token. It can be obtained by looking at requests in web browser development tools. All requests should contain `Authorization` header.

Example below uses curl, which should be available on most Linux machines:

```
curl -X POST 'http://KUSTOSZ_SERVER_ADDRESS/api/v1/entries/manual_add' \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Token 0123456789abcdef0123456789abcdef01234567' \
    -d '{"link": "https://linuxize.com/post/curl-post-request/"}'
```

## Maintenance section

Maintenance section provides views to quickly (de)activate multiple channels at once.

### Stale channels

Channels become stale when Kustosz determines it's no longer possible to access them.

In general, it's normal for resources to become temporarily unavailable - websites are upgraded to new versions, are unable to cope with amount of traffic after going viral on social media, people forget to pay hosting bills. That's why Kustosz will mark channels as stale only if they could not be accessed for extended period of time: during last 10 tries (determined by update frequency) or in last three days, whichever is longer.

It's worth noting that stale channels might have been moved to new URL without leaving proper redirection in place. It's up to you as an user to determine if that is the case.

### Channels without new entries

These channels are online and can be accessed, but have not produced a new entry in number of days (30 by default).

### Inactive channels

These channels have "active" flag turned off. You can activate them back.
