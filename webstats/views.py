# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime

@login_required
def webstats_main_page(request):
  """
  If users are authenticated, direct them to the main page. Otherwise,
  take them to the login page.
  """
  return render_to_response('webstats/index.html')

def webstats_track(request):
  print request

  TRANSPARENT_1_PIXEL_GIF = "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
  return HttpResponse(TRANSPARENT_1_PIXEL_GIF, content_type = "image/gif")
