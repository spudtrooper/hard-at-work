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
  url = 'https://factba.se/rss/calendar-full.json'
  text = util.UrlFetch(url)
  events_json = json.loads(text)
  events = []
  for e in events_json:
    """
    {
      "date": "2018-01-01",
      "time": "07:30:00",
      "time_formatted": "7:30 AM",
      "year": "2018",
      "month": "January",
      "day": "1",
      "day_of_week": "Monday",
      "type": "President Schedule",
      "details": "Out-of-Town Travel Pool Call Time",
      "location": null,
      "coverage": null,
      "daily_text": "In the evening ...",
      "url": null,
      "newmonth": true,
      "daycount": "4",
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
      
