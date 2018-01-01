import helpers
import json
import logging
import os
import re
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.ndb import msgprop
from google.appengine.ext.webapp import template
from datetime import datetime
from datetime import time
from datetime import timedelta
from protorpc import messages

import urllib
import urllib2
import json

from model import Conflict
from model import Event
from model import Tweet

import util

# ----------------------------------------------------------------------
# Utilities
# ----------------------------------------------------------------------

def RenderTemplate(response, name, template_values=None):
  if not template_values:
    template_values = {}
  logging.info('Rendering template[%s] with values[%s]', name, template_values)
  path = os.path.join(os.path.dirname(__file__), 'templates/%s.html' % name)
  response.out.write(template.render(path, template_values))

def RenderTemplateWithOK(response, name, template_values=None):
  logging.info('Rendering with OK template[%s] with values[%s]', 
               name, template_values)
  if not template_values:
    template_values = {}
  path = os.path.join(os.path.dirname(__file__), 'templates/%s.html' % name)
  body = template.render(path, template_values)
  data = {
    'status': 'OK',
    'body': body
  }
  RenderJsonWithOK(response, data)

def RenderJsonWithOK(response, data=None):
  if not data:
    data = {}
  body = {
    'status': 'OK',
    'data': data
  }
  json_data = json.dumps(body)
  response.out.write(json_data)

def GetString(attrs, name):
  v = attrs[name]
  if not v:
    return v
  return helpers.StripAccents(v)

def SanitizeTweet(s):
  # lang="en" data-aria-label-part="0">
  return re.sub('^[^<]+">', '', s)

def ImportTweets(since, until):
  existing_tweets = []
  imported_tweets = []
  if not since:
    since = datetime.now().date() - timedelta(days=1)
  if not until:
    until = since + timedelta(days=2)
  url = ('http://jeffpalm.com/twitterer/twitter.php?'
         'u=realDonaldTrump&since=%s&until=%s' % 
         (str(since), str(until)))
  logging.info('since=%s', since)
  logging.info('until=%s', until)
  logging.info('url=%s', url)
  tweets_text = util.UrlFetch(url)
  logging.info('tweets_text=%s', tweets_text)
  tweets_json = json.loads(tweets_text)
  for tweet in tweets_json['tweets']:
    date_str = GetString(tweet, 'date')
    if not date_str:
      continue
    date = datetime.fromtimestamp(int(date_str))
    text = SanitizeTweet(GetString(tweet, 'text'))
    # user name sometimes starts with /
    user = GetString(tweet, 'user')
    user = re.sub('/', '', user)
    user_id = int(GetString(tweet, 'id'))
    tweet_id = int(GetString(tweet, 'tweetId'))
    img = GetString(tweet, 'img')
    rt = tweet['rt']

    logging.info('date=%s', date)
    logging.info('text=%s', text)
    logging.info('user=%s', user)
    logging.info('user_id=%s', user_id)
    logging.info('tweet_id=%s', tweet_id)
    logging.info('img=%s', img)
    logging.info('rt=%s', rt)

    new_tweet = Tweet(
      date=date, text=text, user=user, user_id=user_id, img=img, 
      rt=rt, tweet_id=tweet_id, hour=date.hour)
    tweets_with_date = db.GqlQuery(
      'SELECT * FROM Tweet WHERE date = :1', date)
    if not tweets_with_date or not any(tweets_with_date):
      logging.info('Adding tweet[%s]', new_tweet)
      new_tweet.put()
      imported_tweets.append(new_tweet)
    else:
      logging.info('Already exists.')
      existing_tweets.append(new_tweet)
  return imported_tweets, existing_tweets

def ImportEvents():
  events = helpers.ImportEvents()

  logging.info('events=[%s]', events)

  imported_events = []
  existing_events = []
  for e in events:
    events_with_date = db.GqlQuery(
      'SELECT * FROM Event WHERE start_date = :1 and end_date = :2',
      e.start_date, e.end_date)
    if not events_with_date or not any(events_with_date):
      logging.info('Adding event[%s]', e)
      e.put()
      imported_events.append(e)
    else:
      logging.info('Already exists.')
      existing_events.append(e)
  return imported_events, existing_events

# ----------------------------------------------------------------------
# Handlers
# ----------------------------------------------------------------------

class IndexPageHandler(webapp.RequestHandler):
  def get(self):
    self.redirect('/conflicts')

class AboutPageHandler(webapp.RequestHandler):
  def get(self):
    RenderTemplate(self.response, 'about')

class TimelinePageHandler(webapp.RequestHandler):
  def get(self):
    date = self.request.get('date') or ''
    logging.info('request date=%s', date)
    template_values = {
      'date': str(date),
    }
    RenderTemplate(self.response, 'timeline', template_values)

class DatesPageHandler(webapp.RequestHandler):
  def get(self):
    events = db.GqlQuery('SELECT * FROM Event')
    tweets = db.GqlQuery('SELECT * FROM Tweet')
    event_dates = list(set([e.start_date.date() for e in events]))
    tweet_dates = list(set([t.date.date() for t in tweets]))
    dates = [e for e in event_dates if e in tweet_dates]
    dates.sort(reverse=True)
    template_values = {
      'dates': [str(d) for d in dates],
      'event_dates': [str(d) for d in event_dates],
      'tweet_dates': [str(d) for d in tweet_dates],
    }
    RenderTemplate(self.response, 'dates', template_values)

class ImportTweetsHandler(webapp.RequestHandler):
  def get(self):
    since = self.request.get('since')
    until = self.request.get('until')
    if since:
      since = datetime.strptime(since, '%Y-%m-%d').date()
    if until:
      until = datetime.strptime(until, '%Y-%m-%d').date()
    imported_tweets, existing_tweets = ImportTweets(since, until)
    template_values = {
      'imported_tweets': imported_tweets,
      'existing_tweets': existing_tweets,
      'num_imported_tweets': len(imported_tweets),
      'num_existing_tweets': len(existing_tweets),
    }
    RenderTemplate(self.response, 'import_tweets', template_values)

class ImportEventsHandler(webapp.RequestHandler):
  def get(self):
    url = self.request.get('url')
    if url:
      logging.info('URL paramenter no longer supported')
    imported_events, existing_events = ImportEvents()
    template_values = {
      'url': url,
      'imported_events': imported_events,
      'existing_events': existing_events,
      'num_imported_events': len(imported_events),
      'num_existing_events': len(existing_events),
    }
    RenderTemplate(self.response, 'import_events', template_values)

class TweetsHandler(webapp.RequestHandler):
  def get(self):
    date = self.request.get('date')
    if date:
      start = datetime.strptime(date, '%Y-%m-%d').date()
      end = start + timedelta(days=1)
      tweets = db.GqlQuery(
        'SELECT * FROM Tweet WHERE date > :1 AND date < :2 '
        'ORDER BY date DESC LIMIT 20', start, end)
    else:
      tweets = db.GqlQuery(
        'SELECT * FROM Tweet ORDER BY date DESC LIMIT 20')
    data = [{
      'text': t.text,
      'date': str(t.date),
      'hour': t.hour,
      'user': t.user,
      'user_id': t.user_id,
      'tweet_id': t.tweet_id,
      'img': t.img,
      'rt': t.rt,
    } for t in tweets]
    RenderJsonWithOK(self.response, data)

class EventsHandler(webapp.RequestHandler):
  def get(self):
    date = self.request.get('date')
    if date:
      start = datetime.strptime(date, '%Y-%m-%d').date()
      end = start + timedelta(days=1)
      events = db.GqlQuery(
        'SELECT * FROM Event WHERE start_date > :1 AND start_date < :2 '
        'ORDER BY start_date DESC LIMIT 20', start, end)
    else:
      events = db.GqlQuery(
        'SELECT * FROM Event ORDER BY start_date DESC LIMIT 20')
    data = []
    for e in events:
      data.append({
        'title': e.title,
        'start_date': str(e.start_date),
        'end_date': str(EndDate(e)),
        'source_url': e.source_url,
      })
    RenderJsonWithOK(self.response, data)

class GetConflictsHandler(webapp.RequestHandler):
  def get(self):
    conflicts = db.GqlQuery('SELECT * FROM Conflict')
    data = []
    for c in conflicts:
      t = c.tweet
      e = c.event
      data.append({
        'tweet_text': t.text,
        'tweet_date': str(t.date),
        'tweet_user': t.user,
        'tweet_user_id': t.user_id,
        'tweet_id': t.tweet_id,
        'tweet_img': t.img,
        'tweet_rt': t.rt,
        'event_title': e.title,
        'event_start_date': str(e.start_date),
        'event_end_date': str(EndDate(e)),
        'event_source_url': e.source_url,
      })
    data = sorted(data, key=lambda c: c['tweet_date'], reverse=True)
    RenderJsonWithOK(self.response, data)

def DeleteAllConflicts():
  try:
    i = 0
    while True:
      logging.info('Deleting conflicts: %d', i)
      q = db.GqlQuery("SELECT __key__ FROM Conflict")
      logging.info('Deleted %d conflicts', q.count())
      assert q.count()
      db.delete(q.fetch(200))
      time.sleep(0.2)
      i += 1
  except Exception, e:
    pass

def EndDate(e):
  end_date = e.end_date
  if not end_date:
    end_date = e.start_date + timedelta(hours=1) - timedelta(minutes=5)
  return end_date

class CreateConflictsHandler(webapp.RequestHandler):
  def get(self):
    tweets = db.GqlQuery('SELECT * FROM Tweet')
    tweet_count = helpers.Len(tweets)
    logging.info('Found %d tweets', tweet_count)

    events = db.GqlQuery('SELECT * FROM Event')
    event_count = helpers.Len(events)
    logging.info('Found %d events', event_count)

    # Map the event dates to list of events.
    event_map = {}
    def Pad(n):
      return '0%d' % n if n < 10 else str(n)
    def Key(d):
      return ':'.join([str(d.year), Pad(d.month), Pad(d.day)])
    for e in events:
      key = Key(e.start_date)
      if key in event_map:
        event_map[key].append(e)
      else:
        event_map[key] = [e]
    logging.info('Printing event map...')
    for k,lst in event_map.iteritems():
      logging.info('%s (%d)', k, len(lst))

    # Create the new conflicts.
    new_conflicts = []
    num_tweet = 0
    for t in tweets:
      num_tweet += 1
      events_for_date = event_map.get(Key(t.date), [])
      logging.info('[%d/%d] Looking at tweet with date %s and found %d events', 
                   num_tweet, tweet_count, t.date, len(events_for_date))
      for e in events_for_date:
        end_date = EndDate(e)
        if e.start_date <= t.date and t.date <= end_date:
          conflict = Conflict(event=e, tweet=t)
          new_conflicts.append(conflict)
          logging.info('Found %s', conflict)
          break

    # There is a race condition between deleting the old conflicts
    # and adding the new ones, but oh well...
    DeleteAllConflicts()

    # Save the new conflicts.
    for c in new_conflicts:
      c.put()

    # Render the result.
    data = {
      'conflict_count': len(new_conflicts),
      'tweet_count': tweet_count,
      'event_count': event_count,
    }
    RenderJsonWithOK(self.response, data)

class DeleteDuplicateEventsHandler(webapp.RequestHandler):
  def get(self):
    events = db.GqlQuery('SELECT * FROM Event')
    event_count = helpers.Len(events)
    logging.info('Found %d events', event_count)

    # Map the event dates to an event. Delete collisions.
    event_map = {}
    def Key(d):
      return ':'.join([str(d.start_date), d.title])
    deleted_event_count = 0
    for e in events:
      key = Key(e)
      if key in event_map:
        logging.info('Deleting event %s', e)
        e.delete()
        deleted_event_count += 1
      else:
        event_map[key] = True

    # Render the result.
    data = {
      'deleted_event_count': deleted_event_count,
      'event_count': event_count,
    }
    RenderJsonWithOK(self.response, data)

class ConflictsPageHandler(webapp.RequestHandler):
  def get(self):
    RenderTemplate(self.response, 'conflicts')

app = webapp.WSGIApplication(
  [('/', IndexPageHandler),
   ('/about', AboutPageHandler),
   ('/timeline', TimelinePageHandler),
   ('/tweets', TweetsHandler),
   ('/events', EventsHandler),
   ('/dates', DatesPageHandler),
   ('/getconflicts', GetConflictsHandler),
   ('/conflicts', ConflictsPageHandler),
 ], debug=True)

cron = webapp.WSGIApplication(
  [('/import_tweets', ImportTweetsHandler),
   ('/import_events', ImportEventsHandler),
   ('/create_conflicts', CreateConflictsHandler),
   ('/delete_duplicate_events', DeleteDuplicateEventsHandler),
 ], debug=True)
