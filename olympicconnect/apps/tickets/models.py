from django.db import models
from django.conf import settings
from apps.events.models import Event
import qrcode
from io import BytesIO
from django.core.files import File

class Ticket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    offer_name = models.CharField(max_length=255)
    ticket_key = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def save(self, *args, **kwargs):
        qr_image = qrcode.make(self.ticket_key)
        buffer = BytesIO()
        qr_image.save(buffer)
        filename = f'ticket_{self.id}.png'
        self.qr_code.save(filename, File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.event.name} - {self.offer_name} - {self.user.email}'
