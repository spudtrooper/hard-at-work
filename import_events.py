# Non-app-engine dependent library to grab events from 
# https://factba.se/topic/calendar.
import datetime
import json
import logging
import re
import util

def ImportEvents():
  """
  Returns: A dict with the same attributes as model.Event.
  """
  url = 'https://media-cdn.factba.se/rss/json/calendar-full.json'
  text = util.UrlFetch(url)
  events_json = json.loads(text)
  events = []
  for e in events_json:
    """
    {
    "date": "2018-07-14",
    "time": null,
    "time_formatted": null,
    "year": "2018",
    "month": "July",
    "day": "14",
    "day_of_week": "Saturday",
    "type": "President Schedule",
    "details": "The President has no public events scheduled.",
    "location": "Trump Turnberry, Girvan, Scotland, United Kingdom",
    "coverage": null,
    "daily_text": null,
    "url": null,
    "newmonth": true,
    "daycount": "2",
    "lastdaily": false
    },
    """
    if e['type'] != 'President Schedule':
      logging.info('Skipping event[%s] because not president\'s schedule', e)
      continue
    title = e['details']
    description = e['daily_text']
    date = e['date']
    if not date:
      logging.info('No date for event[%s]', e)
      continue
    time = e['time']
    if not time:
      logging.info('No time for event[%s]', e)
      continue

    # 2018-01-01: Could also get the parts from individual attributes.
    date_match = re.match('(\d{4})-(\d{2})-(\d{2})', date)
    year = int(date_match.group(1))
    month = int(date_match.group(2))
    day = int(date_match.group(3))   

    # 07:30:00
    time_match = re.match('(\d{2})\:(\d{2})\:(\d{2})', time)
    hour = int(time_match.group(1))
    minute = int(time_match.group(2))

    start_date = datetime.datetime(year, month, day, hour, minute)

    events.append(dict(
      start_date=start_date,
      title=title,
      description=description,
      source_url=url))

  return events
      
