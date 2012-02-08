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

@login_required
def webstats_index(request):
  website_list = Website.objects.all()
  c = Context({
    'website_list': website_list,
  })
  return render_to_response('webstats/index.html',
                            c,
                            context_instance=RequestContext(request))
