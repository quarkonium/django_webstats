# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import Context, loader
from django_webstats.webstats.models import Visitor
from datetime import datetime
from django.template import RequestContext
from django.utils import simplejson
import calendar

@login_required
def webstats_main_page(request):
  """
  If users are authenticated, direct them to the main page. Otherwise,
  take them to the login page.
  """

  #month_array = Visitor.objects.dates('time','month',order='DESC') 

  #months = []
  #for m in month_array:
  #  month = " %s %d " % (calendar.month_name[m.month], m.year)
  #  months.append(month)

  total_visits_array = []
  for m in range(1, 13):
    total_visits_array.append(Visitor.objects.filter(time__year='2012', time__month=m).count())

  unique_visits_array = []
  for m in range(1, 13):
    unique_visits_array.append(Visitor.objects.values('x_ff').distinct().filter(time__year='2012', time__month=m).count())
    
  lu = { 'categories' : ['Jan 2012', 'Feb 2012', 'Mar 2012', 'Apr 2012', 'May 2012', 'Jun 2012', 'Jul 2012', 'Aug 2012', 'Sep 2012', 'Oct 2012', 'Nov 2012', 'Dec 2012'],\
          'total_visits' : total_visits_array,\
          'total_unique_visits' : unique_visits_array }
          
  js_data = simplejson.dumps(lu);

  print js_data

  visitor_list = Visitor.objects.all()
  #t = loader.get_template('webstats/index.html')
  c = Context({
    'visitor_list': visitor_list,
    'js_data': js_data,
  })
  #return render_to_response(t.render(c))
  return render_to_response('webstats/index.html',
                            c,
                            context_instance=RequestContext(request))

webstats_main_page.allow_tags = True

def webstats_track(request):
  print request
  v = Visitor()
  v.x_ff = request.META.get("HTTP_X_FORWARDED_FOR", "")
  v.remote_addr = request.META.get("REMOTE_ADDR", "")
  v.time = datetime.now()
  v.referer = request.META.get("HTTP_REFERER", "")
  v.user_agent = request.META.get("HTTP_USER_AGENT", "")
  v.save() 

  TRANSPARENT_1_PIXEL_GIF = "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
  return HttpResponse(TRANSPARENT_1_PIXEL_GIF, content_type = "image/gif")
