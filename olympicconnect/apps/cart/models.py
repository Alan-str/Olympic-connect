from django.db import models
from django.conf import settings
from apps.events.models import Event

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def get_total_price(self):
        return sum(item.price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='cart_items', on_delete=models.CASCADE)
    offer_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.event.name} - {self.offer_name} - {self.quantity} pcs"
