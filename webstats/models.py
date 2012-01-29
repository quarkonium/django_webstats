from django.db import models

# Create your models here.

class Website(models.Model):
  domain = models.URLField("URL", max_length=200)
  last_activity = models.DateTimeField(auto_now_add=True, editable=False)

class Visitor(models.Model):
  remote_addr = models.IPAddressField(blank=True)
  x_ff        = models.CharField(blank=True, max_length=100)
  time        = models.DateTimeField(auto_now_add=True, editable=False)
  referer     = models.URLField(blank=True, verify_exists=False)
  user_agent  = models.CharField(blank=True, max_length=100)
  website     = models.ForeignKey(Website)
