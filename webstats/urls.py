from django.conf.urls.defaults import *
from webstats.views import *

urlpatterns = patterns('',
  # Main webstats entrance.
  (r'^$', webstats_main_page),
  (r'^$', webstats_track),
)