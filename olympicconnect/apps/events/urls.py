from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.event_list_api, name='event_list_api'),
    path('api/all/', views.all_events_api, name='all_events_api'), 
    path('<int:event_id>/', views.event_info, name='eventinfo'),
    path('all/', views.all_events, name='all_events'), 
]
