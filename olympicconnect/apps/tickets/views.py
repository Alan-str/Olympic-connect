from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Ticket

@login_required
def user_tickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'tickets/ticketlist.html', {'tickets': tickets})
