import sys  
import urllib
import urllib2

def UrlFetch(url, data=None):
  req = urllib2.Request(url, urllib.urlencode(data or {}))
  f = urllib2.urlopen(req)
  response = f.read()
  f.close()
  return response
