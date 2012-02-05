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
from collections import defaultdict


from random import random

import operator
import decimal
import calendar

#Visit = namedtuple("Visit", "time entry_page exit_page")

def unique(seq): 
  checked = []
  for e in seq:
    if e not in checked:
      checked.append(e)
  return checked

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
  page_views_per_visit = []
  entry_statistics = {}
  exit_statistics = {}
  DELTA = timedelta(seconds=30)
  for m in range(1, 13):
    v_a = Visitor.objects.filter(time__year='2012', time__month=m, website__id=id).values('x_ff').distinct()
    number_of_visits = 0

    for v in v_a:
      number_of_visits += 1
      v_times = Visitor.objects.filter(time__year='2012', time__month=m, website__id=id, x_ff=v.get('x_ff')).order_by('time');

      prev = v_times[0]
      entry_statistics[prev.path] = { 'entered' : 1, 'duration' : timedelta(0) }
      current_entry = prev
      entry_page=True
      for t in v_times:
        if t.time - prev.time >= DELTA:
          if entry_page :
            entry_statistics[current_entry.path]['duration'] += t.time - current_entry.time

          if entry_statistics.has_key(t.path) :
            entry_statistics[t.path]['entered'] += 1
            entry_statistics[t.path]['time'] = t.time 
          else:
            entry_statistics[t.path] = { 'entered' : 1, 'duration' : timedelta(0) }
        
	  if exit_statistics.has_key(prev.path) :
	    exit_statistics[prev.path]['exited'] += 1 
	    exit_statistics[prev.path]['duration'] += t.time - prev.time
          else: 
	    exit_statistics[prev.path] = { 'exited' : 1, 'duration' : t.time - prev.time }

	  current_entry = t
	  entry_page = True
        elif t.path != current_entry.path and entry_page :
          entry_statistics[current_entry.path]['duration'] += t.time - current_entry.time
	  entry_page = False
            
          number_of_visits += 1

        prev = t

    total_visits_array.append(number_of_visits)
    if number_of_visits != 0:
      page_views_per_visit.append(Visitor.objects.filter(time__year='2012', time__month=m, website__id=id).count()/(number_of_visits * 1.0))
    else:
      page_views_per_visit.append(0)

  for page in entry_statistics :
    entry_statistics[page]['average'] = timedelta(seconds=round(entry_statistics[page]['duration'].seconds / entry_statistics[page]['entered'] * 1.0))

  for page in exit_statistics :
    exit_statistics[page]['average'] = timedelta(seconds=round(exit_statistics[page]['duration'].seconds / exit_statistics[page]['exited'] * 1.0))

  print sorted(entry_statistics.items(), key=lambda x: x[1]['entered'])

  print entry_statistics
  print exit_statistics

  #for page in exit_page_frequencies:
  #  stats = { "page" : page, "freq" : exit_page_frequencies[page],\
  #            "view_time" : timedelta(seconds=round(total_time_on_exit[page].seconds / (exit_page_frequencies[page] * 1.0))) }
  #  exit_statistics.append(stats)

  unique_visits_array = []
  for m in range(1, 13):
    unique_visits_array.append(Visitor.objects.values('x_ff').distinct().filter(time__year='2012', time__month=m, website__id=id).count())
    
  lu = { 'categories' : ['Jan 2012', 'Feb 2012', 'Mar 2012', 'Apr 2012', 'May 2012', 'Jun 2012', 'Jul 2012', 'Aug 2012', 'Sep 2012', 'Oct 2012', 'Nov 2012', 'Dec 2012'],\
          'total_visits' : total_visits_array,\
          'page_views_per_visit': page_views_per_visit,
          'total_unique_visits' : unique_visits_array }
          
  js_data = simplejson.dumps(lu);

  visitor_list = Visitor.objects.filter(website__id=id).order_by('time')
  w = visitor_list[0].website
  c = Context({
    'visitor_list': visitor_list,
    'website': w,
    'entry_statistics': sorted(entry_statistics.items(), key=lambda x: x[1]['entered'], reverse=True),
    'exit_statistics': sorted(exit_statistics.items(), key=lambda x: x[1]['exited'], reverse=True),
    'js_data': js_data,
  })
  return render_to_response('webstats/webstats.html',
                            c,
                            context_instance=RequestContext(request))

webstats_main_page.allow_tags = True

def webstats_track(request):
  v = Visitor()
  v.x_ff = request.META.get("HTTP_X_FORWARDED_FOR", "")
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
