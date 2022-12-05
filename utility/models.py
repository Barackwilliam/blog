from django.db import models
# Create your models here.

class ShortLink(models.Model):
    url_link = models.URLField(max_length=500, null = True, blank = True)
    shorter_url = models.URLField(null = True, blank = True)

    def __str__(self):
        return self.shorter_url
