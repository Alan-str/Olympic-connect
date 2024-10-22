# models.py
from django.db import models
from django.utils.deconstruct import deconstructible
import os
from uuid import uuid4

@deconstructible
class PathAndRename:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.path, filename)

path_and_rename_thumbnails = PathAndRename('events/thumbnails/')
path_and_rename_banners = PathAndRename('events/banners/')

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    price_solo = models.DecimalField(max_digits=10, decimal_places=2)
    price_duo = models.DecimalField(max_digits=10, decimal_places=2)
    price_family = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(upload_to=path_and_rename_thumbnails)
    banner = models.ImageField(upload_to=path_and_rename_banners)

    def __str__(self):
        return self.name
