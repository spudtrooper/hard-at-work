import logging
import re
import datetime
import urllib
import urllib2
import unicodedata

import model

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

def Len(result):
  res = 0
  for _ in result:
    res += 1
  return res

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def StripAccents(v):
  if not v:
    return v
  return strip_accents(unicode(v))

def ImportEvents(url):
  existing_events = []
  imported_events = []
  events_text = UrlFetch(url)
  month = None
  day = None
  year = None
  events = []
  for line in events_text.split('\n'):

    # <strong>10:40AM</strong>
    match = re.match('.*<strong>\s*(\d\d?):(\d\d?)([AP]M)\s*</strong>\s*:\s*([^<]+)', line)
    if match:
      hour = int(match.group(1))
      minute = int(match.group(2))
      am_pm = match.group(3)
      title = StripAccents(match.group(4))
      if am_pm == 'PM' and hour < 12:
        hour += 12
      logging.info('Have simple time %s:%s', hour, minute)
      start_date = datetime.datetime(year, month, day, hour, minute)
      event = model.Event(start_date=start_date, title=title, source_url=url)
      events.append(event)
      continue

    # <strong><span style="font-family:&quot;Arial&quot;,sans-serif">9:30 AM:</span>\
    # </strong> President Trump speaks to President Recep Tayyip Erdogan of Turkey</p>
    match = re.match('.*<strong><span style="font-family:&quot;Arial&quot;,sans-serif">'
                     '\s*(\d\d?):(\d\d?) ([AP]M)\s*:\s*</span></strong>(.*)</p>', line)
    if match:
      if not month:
        raise Exception('No month yet')
      hour = int(match.group(1))
      minute = int(match.group(2))
      am_pm = match.group(3)
      title = StripAccents(match.group(4))
      logging.info('hour=%s', hour)
      logging.info('minute=%s', minute)
      logging.info('am_pm=%s', am_pm)
      logging.info('title=%s', title)
      if am_pm == 'PM' and hour < 12:
        hour += 12
      start_date = datetime.datetime(year, month, day, hour, minute)
      event = model.Event(start_date=start_date, title=title, source_url=url)
      events.append(event)
      continue

    #   <title>1600 Daily: Everything White House for 6/30/17 | whitehouse.gov</title>
    match = re.match('.*<title>.*(\d\d?)/(\d\d?)/(\d{2}\d?\d?)[^<]+</title>', line)
    if match:
      m = match.group(1)
      d = match.group(2)
      y = match.group(3)
      logging.info('m=%s', m)
      logging.info('d=%s', d)
      logging.info('y=%s', y)
      day = int(d)
      month = int(m)
      year = int(y)
      if year < 2000:
        year += 2000
      logging.info('month=%s', month)
      logging.info('day=%s', day)
      logging.info('year=%s', year)
      continue

  # Assign end dates.
  i = 0
  while i < len(events) - 1:
    e1 = events[i]
    e2 = events[i + 1]
    e1.end_date = e2.start_date
    i += 1

  logging.info('events=[%s]', events)

  return events

def UrlFetch(url, data=None):
  req = urllib2.Request(url, urllib.urlencode(data or {}))
  f = urllib2.urlopen(req)
  response = f.read()
  f.close()
  return response
