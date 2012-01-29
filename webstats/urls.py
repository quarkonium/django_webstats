from django.conf.urls.defaults import *
from webstats.views import *

urlpatterns = patterns('',
  # Main webstats entrance.
  (r'track/', webstats_track),
  #(r'main/', webstats_main_page),
  (r'^main/(\d+)$', 'django_webstats.webstats.views.webstats_main_page'),
  (r'^$', webstats_index),
)
