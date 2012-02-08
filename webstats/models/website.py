from django.db import models

class Website(models.Model):
  domain = models.URLField("URL", max_length=200)
  last_activity = models.DateTimeField(auto_now_add=True, editable=False)

  class Meta:
    app_label = 'webstats'
