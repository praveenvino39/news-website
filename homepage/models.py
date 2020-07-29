from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class SavedNew(models.Model):
    user = models.CharField(max_length=100)
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    urlToImage = models.URLField(blank=True)
    url = models.URLField()
    date = models.CharField(max_length=20, blank=True)
    source = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.title


