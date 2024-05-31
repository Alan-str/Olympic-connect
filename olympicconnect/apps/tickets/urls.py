from django.urls import path
from . import views

urlpatterns = [
    path('ticketlist/', views.user_tickets, name='user_tickets'),
]
