# Frontend

Frontend configuration can be changed in web UI, by accessing "Settings" at the bottom of navigation panel.

## Theme

You can choose between Light and Dark themes.

## Automatically mark article as read

You can decide when article should be marked as read automatically, if ever. Available options:

* "Never" - disables automatic marking of articles.
* "Upon opening" - article will be marked as read immediately when you open it.
* "When opened for X seconds" - article will be marked as read when it is opened for specified number of seconds. If you close the article before timer runs out, it will not be marked as read. Timer starts from beginning when you open the same article again.
* "When X% has been read" - article will be marked as read once you scroll past the specified proportion of article content. 100% is special and means "as soon as the bottom of article is visible". Except 100%, values above 70% might be hard to trigger on short articles.

## Behavior

### Always keep opened entry on top of list

When this options is checked, article will scroll up to the top of the screen when it is opened. This only matters for articles at the top half of the screen, as articles below them will be always scrolled up.
