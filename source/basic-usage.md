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

## Using local file as channel source

Kustosz can read content from any XML file that follows RSS or ATOM specification. While most of these files are delivered through web, you can use local file as well. This way Kustosz can read any content source it does not handle natively - as long as you can transform it into RSS or ATOM file.

First, save XML files inside the directory specified by `FEED_FETCHER_LOCAL_FEEDS_DIR` setting (FIXME by default). You can create directories inside to organize your files. Then, run following command:

```
kustosz-manager import_channels --wait autodiscover
```

If you add new files in the future, just re-run the command.

## Deactivating a channel

When modifying a channel, you can toggle "active" flag. When "active" flag is disabled (channel is not active), it will not be checked for new content during channels update. 

Deactivating a channel is intermediate step before removing it. Channel is not checked for new content, but all past content is still available in the application. This is especially useful for channels that disappeared from the web, stopped being updated or are very active and you want to silent them for a while.

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
