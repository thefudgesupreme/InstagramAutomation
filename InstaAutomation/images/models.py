import time
from django.db import models
from django.conf import settings
from django.utils.text import slugify
import os, datetime
# Create your models here.

class Image(models.Model):
    title=models.CharField(max_length=100,blank=True)
    description=models.CharField(max_length=500,blank=True)
    slug = models.SlugField(unique=True,blank=True,)
    datetime = models.DateTimeField(default=datetime.datetime.now)
    imgur_uploaded = models.BooleanField(default=False)
    imgur_url = models.URLField(blank=True)
    image = models.ImageField(default='fallback.png',blank=False, upload_to=os.path.join(settings.MEDIA_ROOT,'images'))


    def save(self, *args, **kwargs) -> None:
        if self.slug == "":
            time.sleep(1)
            self.slug = slugify(hash(self.title+self.datetime.strftime('%m%d%Y-%H%M%S')), allow_unicode=True)
        return super().save()
        