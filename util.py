import sys  
import logging

from google.appengine.api import urlfetch

def UrlFetch(url, data=None):
  try:
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      return result.content
    else:
      logging.info('code: %d', result.status_code)
  except urlfetch.Error:
    logging.exception('Caught exception fetching url')

  return None
