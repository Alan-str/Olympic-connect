from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Event

def event_list_api(request):
    events = Event.objects.all()[:3]
    event_list = []
    for event in events:
        event_list.append({
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'thumbnail': event.thumbnail.url 
        })
    return JsonResponse(event_list, safe=False)

def all_events_api(request):
    events = Event.objects.all()  # Récupérer tous les événements
    event_list = []
    for event in events:
        event_list.append({
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'thumbnail': event.thumbnail.url
        })
    return JsonResponse(event_list, safe=False)

def all_events(request):
    events = Event.objects.all()  
    return render(request, 'events/allevents.html', {'events': events})

def event_info(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/eventinfo.html', {'event': event})