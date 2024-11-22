from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.cart.models import Cart, CartItem
from apps.events.models import Event

User = get_user_model()


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@exemple.com",
            username="testuser",
            password="password123"
        )

        self.event1 = Event.objects.create(
            name="Event 1",
            description="Description Event 1",
            date="2024-02-01",
            price_solo=Decimal("20.00"),
            price_duo=Decimal("35.00"),
            price_family=Decimal("50.00")
        )
        self.event2 = Event.objects.create(
            name="Event 2",
            description="Description Event 2",
            date="2024-03-01",
            price_solo=Decimal("30.00"),
            price_duo=Decimal("60.00"),
            price_family=Decimal("90.00")
        )

        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=self.cart,
            event=self.event1,
            offer_name="Solo",
            price=self.event1.price_solo,
            quantity=1
        )
        CartItem.objects.create(
            cart=self.cart,
            event=self.event2,
            offer_name="Solo",
            price=self.event2.price_solo,
            quantity=1
        )

    def test_cart_total_price(self):
        expected_total = (self.event1.price_solo) + (self.event2.price_solo)
        self.assertEqual(self.cart.get_total_price(), expected_total)


class CartViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@exemple.com",
            username="testuser",
            password="password123"
        )
        self.client.login(email="test@exemple.com", password="password123")

        self.event = Event.objects.create(
            name="Test Event",
            description="Description Test Event",
            date="2024-03-01",
            price_solo=Decimal("15.00"),
            price_duo=Decimal("25.00"),
            price_family=Decimal("35.00")
        )

        self.cart = Cart.objects.create(user=self.user)

    def test_add_to_cart_view(self):
        response = self.client.post(
            reverse("add_to_cart", args=[self.event.id]),
            data={"price": "15.00", "offer_name": "Solo"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().price, Decimal("15.00"))

    def test_cart_detail_view(self):
        response = self.client.get(reverse("cart_detail"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cartdetails.html')

    def test_remove_from_cart_view(self):
        cart_item = CartItem.objects.create(
            cart=self.cart,
            event=self.event,
            offer_name="Solo",
            price=self.event.price_solo,
            quantity=1
        )
        response = self.client.post(reverse("remove_from_cart", args=[cart_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart.items.count(), 0)

    def test_process_payment_view(self):
        CartItem.objects.create(
            cart=self.cart,
            event=self.event,
            offer_name="Solo",
            price=self.event.price_solo,
            quantity=1
        )
        response = self.client.post(reverse("process_payment"))
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(self.cart.items.count(), 0)  
