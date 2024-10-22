# models.py in the tickets app
from django.db import models
from django.conf import settings
from apps.events.models import Event
import qrcode
from io import BytesIO
from django.core.files import File
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible

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

path_and_rename_qr_codes = PathAndRename('qr_codes/')

class Ticket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    offer_name = models.CharField(max_length=255)
    ticket_key = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to=path_and_rename_qr_codes, blank=True)

    def save(self, *args, **kwargs):
        qr_image = qrcode.make(self.ticket_key)
        buffer = BytesIO()
        qr_image.save(buffer)
        filename = f'ticket_{self.id}.png'
        self.qr_code.save(filename, File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.event.name} - {self.offer_name} - {self.user.email}'
