from django_webstats.views import *
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
  (r'^$', main_page),

  # Login / logout.
  (r'^login/$', 'django.contrib.auth.views.login'),
  (r'^logout/$', logout_page),

  # webstats
  (r'^webstats/', include('webstats.urls')),

  # Serve static content.
  (r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': 'static'}),
  )

if settings.DEBUG:
  # static files (images, css, javascript, etc.)
  urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
      'document_root': settings.MEDIA_ROOT}))
