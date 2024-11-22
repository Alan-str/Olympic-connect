from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from apps.events.models import Event
from apps.tickets.models import Ticket
from decimal import Decimal, InvalidOperation
import random
import string


def generate_unique_key(length=7):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# @login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cartdetails.html', {'cart': cart})

@login_required(login_url='/accounts/login/')
def add_to_cart(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    price = request.POST.get('price')
    offer_name = request.POST.get('offer_name')

    try:
        clean_price = price.replace(',', '.').replace('\xa0', '').strip()
        price = Decimal(clean_price)
    except InvalidOperation:
        return JsonResponse({'success': False, 'error': 'Invalid price format'})

    CartItem.objects.create(cart=cart, event=event, offer_name=offer_name, price=price)

    return JsonResponse({'success': True, 'cart_total': cart.get_total_price()})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return JsonResponse({'success': True, 'cart_total': cart_item.cart.get_total_price()})

@login_required
def process_payment(request):
    cart = Cart.objects.get(user=request.user)
    if cart.items.exists():
        for item in cart.items.all():
            event = item.event
            offer_name = item.offer_name
            new_key= generate_unique_key()
            ticket_key = f"{request.user.security_key}_{new_key}"

            Ticket.objects.create(
                user=request.user,
                event=event,
                offer_name=offer_name,
                ticket_key=ticket_key,
            )
        cart.items.all().delete()

    return redirect('user_tickets')