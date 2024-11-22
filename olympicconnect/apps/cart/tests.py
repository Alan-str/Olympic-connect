from django.test import TestCase, Client
from django.urls import reverse
from apps.cart.models import Cart, CartItem
from apps.events.models import Event
from django.contrib.auth import get_user_model
from datetime import date
from decimal import Decimal

User = get_user_model()


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@exemple.com",
            password="password123"
        )
        self.cart = Cart.objects.create(user=self.user)
        self.event1 = Event.objects.create(
            name="Event 1",
            description="Description 1",
            date=date(2024, 1, 1),
            price_solo=Decimal("20.00"),
            price_duo=Decimal("35.00"),
            price_family=Decimal("50.00")
        )
        self.event2 = Event.objects.create(
            name="Event 2",
            description="Description 2",
            date=date(2024, 2, 1),
            price_solo=Decimal("30.00"),
            price_duo=Decimal("45.00"),
            price_family=Decimal("60.00")
        )
        CartItem.objects.create(cart=self.cart, event=self.event1, price=Decimal("20.00"), quantity=2)
        CartItem.objects.create(cart=self.cart, event=self.event2, price=Decimal("30.00"), quantity=1)

    def test_cart_total_price(self):
        self.assertEqual(self.cart.get_total_price(), Decimal("70.00"))


class CartViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Créez un utilisateur
        self.user = User.objects.create_user(
            username="testuser",
            email="test@exemple.com",
            password="password123"
        )

        # Créez un événement
        self.event = Event.objects.create(
            name="Test Event",
            description="Test Description",
            date=date(2024, 3, 1),
            price_solo=Decimal("15.00"),
            price_duo=Decimal("25.00"),
            price_family=Decimal("40.00")
        )

        # Créez un panier
        self.cart = Cart.objects.create(user=self.user)

    def test_add_to_cart_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("add_to_cart", args=[self.event.id]),
            data={"price": "15.00", "offer_name": "Test Offer"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().price, Decimal("15.00"))

    def test_cart_detail_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("cart_detail"))
        self.assertEqual(response.status_code, 200)

    def test_remove_from_cart_view(self):
        self.client.login(username="testuser", password="password123")
        cart_item = CartItem.objects.create(cart=self.cart, event=self.event, price=Decimal("15.00"))
        response = self.client.post(reverse("remove_from_cart", args=[cart_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_process_payment_view(self):
        self.client.login(username="testuser", password="password123")
        CartItem.objects.create(cart=self.cart, event=self.event, price=Decimal("15.00"))
        response = self.client.post(reverse("process_payment"))
        self.assertEqual(response.status_code, 302)  # Redirection après succès
        self.assertEqual(self.cart.items.count(), 0)  # Vérifiez que le panier est vide
