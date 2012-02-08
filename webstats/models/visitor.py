from django.db import models
from webstats.models.website import Website

class Visitor(models.Model):
  remote_addr = models.IPAddressField(blank=True)
  x_ff        = models.CharField(blank=True, max_length=100)
  time        = models.DateTimeField(auto_now_add=True, editable=False)
  referer     = models.URLField(blank=True, verify_exists=False)
  user_agent  = models.CharField(blank=True, max_length=100)
  path        = models.CharField(blank=True, max_length=100)
  website     = models.ForeignKey(Website)

  class Meta:
    app_label = 'webstats'
