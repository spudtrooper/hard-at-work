import import_events
import logging
import re
import datetime
import unicodedata
import util

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

def ImportEvents():
  return [model.Event(start_date=e['start_date'], 
                      title=e['title'], 
                      description=e['description'], 
                      source_url=e['source_url']) 
          for e in import_events.ImportEvents()]
