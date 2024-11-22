from django.test import TestCase
from django.urls import reverse
from apps.tickets.models import Ticket
from apps.events.models import Event
from django.contrib.auth import get_user_model

User = get_user_model()

class TicketViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@exemple.com",
            password="password123"
        )
        self.event = Event.objects.create(
            name="Test Event",
            description="This is a test event.",
            date="2024-12-31",
            price_solo=10.00,
            price_duo=18.00,
            price_family=25.00,
            thumbnail="path/to/thumbnail.jpg",
            banner="path/to/banner.jpg",
        )
        self.ticket = Ticket.objects.create(
            event=self.event,
            user=self.user,
        )

    def test_user_tickets_view(self):
        login_successful = self.client.login(email="test@exemple.com", password="password123")
        self.assertTrue(login_successful, "L'utilisateur n'a pas pu se connecter.")

        response = self.client.get(reverse("user_tickets"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tickets/ticketlist.html")
        self.assertContains(response, self.event.name)
