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

# ----------------------------------------------------------------------
# Model
# ----------------------------------------------------------------------

class Tweet(db.Model):
  text = db.StringProperty(multiline=True)
  date = db.DateTimeProperty()
  user = db.StringProperty()
  user_id = db.IntegerProperty()
  tweet_id = db.IntegerProperty()
  img = db.StringProperty()
  rt = db.BooleanProperty()
  hour = db.IntegerProperty()

class Event(db.Model):
  start_date = db.DateTimeProperty()
  title = db.StringProperty(multiline=True)
  end_date = db.DateTimeProperty()
  source_url = db.StringProperty()

class Conflict(db.Model):
  event = db.ReferenceProperty(Event,
                               required=True,
                               collection_name='events')
  tweet = db.ReferenceProperty(Tweet,
                               required=True,
                               collection_name='tweets')
  date = db.DateTimeProperty(auto_now_add=True)
