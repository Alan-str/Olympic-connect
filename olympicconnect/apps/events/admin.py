from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'price_solo', 'price_duo', 'price_family')
    search_fields = ('name',)
    list_filter = ('date',)
