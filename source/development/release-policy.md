# Release policy

Kustosz aims for monthly release schedule, with [version numbers based on calendar](https://calver.org/).

We use `YY.MM.PATCH` version numbering scheme, where `YY` are last two digits of release year, `MM` are two digits for release month and `PATCH` is zero-based index of release in given month. "22.01.0" is first release in January 2022, "22.12.2" is third release in December 2022.

We release new version every time there are any changes in `main` branch at the time release decision is made, as compared to last release. If there are no changes, month is skipped.

`PATCH` releases are reserved for extraordinary situations that warrant a release outside of usual schedule. These could be packaging issue that make new version uninstallable or very serious regressions. Decision about PATCH releases is made on case-by-case basis.

There are no long-term support versions.

Frontend and backend are developed independently and their version numbers may be different.

Users are advised to always use the newest versions of frontend and backend code available at the time of installation or upgrade. Configurations that use older version of one of the components are not supported. However, developers should make changes in backwards-compatible manner where possible.
