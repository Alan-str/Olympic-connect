from django.shortcuts import render
from apps.events.models import Event



def index(request):
    events = Event.objects.all()[:3] 
    return render(request, 'index.html', {'events': events})

