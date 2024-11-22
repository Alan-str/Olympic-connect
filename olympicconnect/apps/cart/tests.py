from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth import get_user_model
from apps.cart.models import Cart, CartItem
from apps.events.models import Event

User = get_user_model()

# --- TESTS POUR LES MODÈLES ---
class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@exemple.com", password="password123")
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_total_price(self):
        event1 = Event.objects.create(name="Event 1", price=20.00)
        event2 = Event.objects.create(name="Event 2", price=30.00)
        CartItem.objects.create(cart=self.cart, event=event1, price=20.00, quantity=2)
        CartItem.objects.create(cart=self.cart, event=event2, price=30.00, quantity=1)

        self.assertEqual(self.cart.get_total_price(), 70.00)

class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@exemple.com", password="password123")
        self.cart = Cart.objects.create(user=self.user)
        self.event = Event.objects.create(name="Test Event", price=10.00)

    def test_cart_item_str_representation(self):
        cart_item = CartItem.objects.create(cart=self.cart, event=self.event, offer_name="Special Offer", price=10.00, quantity=3)
        self.assertEqual(str(cart_item), "Test Event - Special Offer - 3 pcs")

# --- TESTS POUR LES VUES ---
class CartViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@exemple.com", password="password123")
        self.event = Event.objects.create(name="Test Event", price=15.00)

    def test_cart_detail_view(self):
        self.client.login(email="test@exemple.com", password="password123")
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cartdetails.html')

    def test_add_to_cart_view(self):
        self.client.login(email="test@exemple.com", password="password123")
        response = self.client.post(
            reverse('add_to_cart', args=[self.event.id]),
            data={"price": "15.00", "offer_name": "Test Offer"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().price, Decimal("15.00"))

    def test_remove_from_cart_view(self):
        self.client.login(email="test@exemple.com", password="password123")
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, event=self.event, offer_name="Test Offer", price=15.00)
        response = self.client.post(reverse('remove_from_cart', args=[cart_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_process_payment_view(self):
        self.client.login(email="test@exemple.com", password="password123")
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, event=self.event, offer_name="Test Offer", price=15.00)

        response = self.client.post(reverse('process_payment'))
        self.assertEqual(response.status_code, 302)  # Redirection après succès
        self.assertEqual(cart.items.count(), 0)  # Le panier doit être vidé
