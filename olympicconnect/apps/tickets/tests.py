from django.test import TestCase, Client
from django.urls import reverse
from apps.tickets.models import Ticket
from apps.events.models import Event
from django.contrib.auth import get_user_model
from datetime import date
from decimal import Decimal

User = get_user_model()


class TicketViewsTest(TestCase):
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
            description="Test Event Description",
            date=date(2024, 1, 1),
            price_solo=Decimal("20.00"),
            price_duo=Decimal("35.00"),
            price_family=Decimal("50.00")
        )

        # Créez un ticket
        self.ticket = Ticket.objects.create(
            user=self.user,
            event=self.event,
            offer_name="Solo",
            ticket_key="12345TESTKEY"
        )

    def test_user_tickets_view(self):
        # Connexion de l'utilisateur
        login_successful = self.client.login(username="testuser", password="password123")
        self.assertTrue(login_successful, "L'utilisateur n'a pas pu se connecter.")
        
        # Requête à la vue
        response = self.client.get(reverse("user_tickets"))

        # Test de la réponse
        self.assertEqual(response.status_code, 200)  # La vue doit renvoyer 200
        self.assertTemplateUsed(response, "tickets/user_tickets.html")
        self.assertContains(response, self.event.name)
        self.assertContains(response, self.ticket.offer_name)
