# Create your views here.
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
from random import random

import calendar


#Visit = namedtuple("Visit", "time entry_page exit_page")

@login_required
def webstats_index(request):
  website_list = Website.objects.all()
  c = Context({
    'website_list': website_list,
  })
  return render_to_response('webstats/index.html',
                            c,
                            context_instance=RequestContext(request))

@login_required
def webstats_main_page(request, id):
  """
  If users are authenticated, direct them to the main page. Otherwise,
  take them to the login page.
  """

  #month_array = Visitor.objects.dates('time','month',order='DESC') 

  #months = []
  #for m in month_array:
  #  month = " %s %d " % (calendar.month_name[m.month], m.year)
  #  months.append(month)

  #Visits, 60min interval for given visitor
  total_visits_array = []
  delta = timedelta(hours=1)
  for m in range(1, 13):
    v_a = Visitor.objects.filter(time__year='2012', time__month=m, website__id=id).values('x_ff').distinct()
    number_of_visits = 0
    for v in v_a:
      number_of_visits += 1
      v_times = Visitor.objects.filter(time__year='2012', time__month=m, website__id=id, x_ff=v.get('x_ff')).order_by('time');
      last = v_times[0].time
      for t in v_times:
        diff = t.time - last
        if diff >= delta:
          number_of_visits += 1
        last = t.time
      
    total_visits_array.append(number_of_visits)

  unique_visits_array = []
  for m in range(1, 13):
    unique_visits_array.append(Visitor.objects.values('x_ff').distinct().filter(time__year='2012', time__month=m, website__id=id).count())
    
  lu = { 'categories' : ['Jan 2012', 'Feb 2012', 'Mar 2012', 'Apr 2012', 'May 2012', 'Jun 2012', 'Jul 2012', 'Aug 2012', 'Sep 2012', 'Oct 2012', 'Nov 2012', 'Dec 2012'],\
          'total_visits' : total_visits_array,\
          'total_unique_visits' : unique_visits_array }

  print "unique"
  print unique_visits_array
  print "total"
  print total_visits_array
          
  js_data = simplejson.dumps(lu);

  #test_stats = Visit(datetime.now(), "entry", "exit")
  #print test_stats.time

  visitor_list = Visitor.objects.filter(website__id=id)
  w = visitor_list[0].website
  c = Context({
    'visitor_list': visitor_list,
    'website': w,
    'js_data': js_data,
  })
  return render_to_response('webstats/webstats.html',
                            c,
                            context_instance=RequestContext(request))

webstats_main_page.allow_tags = True

def webstats_track(request):
  #print request
  v = Visitor()
  #v.x_ff = request.META.get("HTTP_X_FORWARDED_FOR", "")
  v.x_ff = "131.169.40.%d" % (random() * 10)
  v.remote_addr = request.META.get("REMOTE_ADDR", "")
  v.time = datetime.now()
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
