from django.conf.urls.defaults import *
from webstats.views import *

urlpatterns = patterns('',
  # Main webstats entrance.
  (r'track/', webstats_track),
  (r'^$', webstats_main_page),
)
