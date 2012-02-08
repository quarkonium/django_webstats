from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import Context, loader
from django_webstats.webstats.models import Website
from django_webstats.webstats.models import Visitor
from datetime import datetime
from datetime import timedelta
from django.template import RequestContext
from django.utils import simplejson
from urlparse import urlparse
from collections import namedtuple
from collections import defaultdict
from xml.dom import minidom
from random import random

import urllib
import operator
import decimal
import calendar
from webstats.models.website import Website
from webstats.models.visitor import Visitor

def webstats_track(request):
  v = Visitor()
  v.x_ff = request.META.get("HTTP_X_FORWARDED_FOR", "")
  v.remote_addr = request.META.get("REMOTE_ADDR", "")

  now = datetime.now()
  delta = (0 if now.microsecond < 500000 else 1000000) - now.microsecond

  v.time = now + timedelta(microseconds=delta)

  v.referer = request.META.get("HTTP_REFERER", "")
  v.user_agent = request.META.get("HTTP_USER_AGENT", "")

  url = urlparse(v.referer)
  v.path = url.path
  
  w_array = Website.objects.filter(domain=url.netloc)
  if len(w_array) == 0:
    w = Website()
    w.domain = url.netloc
    w.last_activity=datetime.now()
    w.save()
    v.website_id=w.id
  else:
    v.website_id=w_array[0].id
    w_array[0].last_activity=datetime.now()
    w_array[0].save()

  v.save() 

  TRANSPARENT_1_PIXEL_GIF = "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
  return HttpResponse(TRANSPARENT_1_PIXEL_GIF, content_type = "image/gif")
