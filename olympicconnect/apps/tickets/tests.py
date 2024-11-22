from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.tickets.models import Ticket
from apps.events.models import Event
from django.contrib.auth import get_user_model
from datetime import date
from decimal import Decimal

User = get_user_model()

# --- TESTS POUR LES MODÈLES ---
class TicketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@exemple.com", password="password123")
        self.event = Event.objects.create(
            name="Test Event",
            description="A test event",
            date=date(2024, 1, 1),
            price_solo=Decimal("10.00"),
            price_duo=Decimal("18.00"),
            price_family=Decimal("25.00"),
            thumbnail=SimpleUploadedFile("thumbnail.jpg", b"file_content", content_type="image/jpeg"),
            banner=SimpleUploadedFile("banner.jpg", b"file_content", content_type="image/jpeg")
        )
        self.ticket = Ticket.objects.create(
            user=self.user,
            event=self.event,
            offer_name="Special Offer",
            ticket_key="TEST123"
        )

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.user, self.user)
        self.assertEqual(self.ticket.event, self.event)
        self.assertEqual(self.ticket.offer_name, "Special Offer")
        self.assertEqual(self.ticket.ticket_key, "TEST123")
        self.assertTrue(self.ticket.qr_code.name.endswith(".png"))

    def test_ticket_str_representation(self):
        self.assertEqual(str(self.ticket), "Test Event - Special Offer - test@exemple.com")

# --- TESTS POUR LES VUES ---
class TicketViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email="test@exemple.com", password="password123")
        self.event = Event.objects.create(
            name="Test Event",
            description="A test event",
            date=date(2024, 1, 1),
            price_solo=Decimal("10.00"),
            price_duo=Decimal("18.00"),
            price_family=Decimal("25.00"),
            thumbnail=SimpleUploadedFile("thumbnail.jpg", b"file_content", content_type="image/jpeg"),
            banner=SimpleUploadedFile("banner.jpg", b"file_content", content_type="image/jpeg")
        )
        Ticket.objects.create(
            user=self.user,
            event=self.event,
            offer_name="Special Offer",
            ticket_key="TEST123"
        )

    def test_user_tickets_view(self):
        self.client.login(email="test@exemple.com", password="password123")
        response = self.client.get(reverse("user_tickets"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tickets/ticketlist.html")
        self.assertContains(response, "Test Event")
        self.assertContains(response, "Special Offer")
