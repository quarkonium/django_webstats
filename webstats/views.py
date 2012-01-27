# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import Context, loader
from django_webstats.webstats.models import Visitor
from datetime import datetime
from django.template import RequestContext
from django.utils import simplejson

@login_required
def webstats_main_page(request):
  """
  If users are authenticated, direct them to the main page. Otherwise,
  take them to the login page.
  """

  lu = { 'days' : [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],\
          'total_visits' : [18, 22, 30, 34, 40, 47],\
          'total_unique_visits' : [1, 2, 4, 4, 5, 7] }
          
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
  #v.ip = request.META.get("HTTP_X_FORWARDED_FOR", "") #get visitor ip
  v.ip = request.META.get("REMOTE_ADDR", "") #get visitor ip
  v.time = datetime.now() # get visitor time
  v.referer = request.META.get("HTTP_REFERER", "") #get visitor referer
  v.user_agent = request.META.get("HTTP_USER_AGENT", "") # get visitor user agent
  v.save() 

  TRANSPARENT_1_PIXEL_GIF = "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
  return HttpResponse(TRANSPARENT_1_PIXEL_GIF, content_type = "image/gif")
