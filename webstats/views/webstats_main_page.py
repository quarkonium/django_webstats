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

GEO_IP_LOOKUP_URL = 'http://api.hostip.info/?ip=%s'
GML_NS = 'http://www.opengis.net/gml'

def unique(seq): 
  checked = []
  for e in seq:
    if e not in checked:
      checked.append(e)
  return checked


def ip_location_lookup(ip):
  """
  Look up the location information based on the IP address passed in
  """
  dom = minidom.parse(urllib.urlopen(GEO_IP_LOOKUP_URL % ip))
  e = dom.getElementsByTagName('Hostip')[0]
  location = e.getElementsByTagNameNS(GML_NS, 'name')[0].firstChild.data.partition(',')

  try:
    latlong = e.getElementsByTagNameNS(GML_NS, 'coordinates')[0].firstChild.data.partition(',')
  except:
    latlong = None

  return {
    'country_code': e.getElementsByTagName('countryAbbrev')[0].firstChild.data,
    'country_name': e.getElementsByTagName('countryName')[0].firstChild.data,
    'locality': location[0].strip(),
    'region': location[2].strip(),
    'longitude': latlong[0].strip() if latlong else '',
    'latitude': latlong[2].strip() if latlong else ''
  }




@login_required
def webstats_main_page(request, id):
 
  #Visits, session is deemed to be ended after 60min of inactivity 
  location_data = {}
  total_visits_array = []
  page_views_per_visit = []
  entry_statistics = {}
  exit_statistics = {}
  DELTA = timedelta(seconds=30)
  for m in range(1, 13) :
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
