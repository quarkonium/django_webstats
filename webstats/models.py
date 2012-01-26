from django.db import models

# Create your models here.
class Visitor(models.Model):
  page = models.CharField(blank=True, max_length=100)
  ip = models.IPAddressField(blank=True)
  time = models.DateTimeField(auto_now_add=True, editable=False)
  referer = models.URLField(blank=True, verify_exists=False)
  user_agent = models.CharField(blank=True, max_length=100)
