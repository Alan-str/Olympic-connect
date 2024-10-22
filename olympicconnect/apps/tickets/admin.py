from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class Ticket(admin.ModelAdmin):
    list_display = ('user', 'event', 'offer_name', 'ticket_key', 'qr_code')


