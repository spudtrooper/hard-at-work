This is a site to join Presidential tweets with official meetings.

## Live

http://hard-at-work.appspot.com

## About

The following cron jobs import data:

* `/import_tweets` - Imports tweets from twitter via a proxy site
* `/import_events` - Imports events from
  https://factba.se/topic/calendar
* `/create_conflicts` - Joins tweets and events imported from above

The timeline used [visjs](http://visjs.org).
