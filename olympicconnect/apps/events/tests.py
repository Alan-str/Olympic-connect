from django.test import TestCase, Client
from django.urls import reverse
from apps.events.models import Event
from datetime import date
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile

# --- TESTS POUR LES MODÈLES ---
class EventModelTest(TestCase):
    def setUp(self):
        self.thumbnail = SimpleUploadedFile("thumbnail.jpg", b"file_content", content_type="image/jpeg")
        self.banner = SimpleUploadedFile("banner.jpg", b"file_content", content_type="image/jpeg")
        self.event = Event.objects.create(
            name="Test Event",
            description="A test event",
            date=date(2024, 1, 1),
            price_solo=Decimal("10.00"),
            price_duo=Decimal("18.00"),
            price_family=Decimal("25.00"),
            thumbnail=self.thumbnail,
            banner=self.banner
        )

    def test_event_creation(self):
        self.assertEqual(self.event.name, "Test Event")
        self.assertEqual(self.event.description, "A test event")
        self.assertEqual(self.event.price_solo, Decimal("10.00"))
        self.assertEqual(self.event.price_duo, Decimal("18.00"))
        self.assertEqual(self.event.price_family, Decimal("25.00"))
        self.assertEqual(self.event.date, date(2024, 1, 1))

    def test_event_str_representation(self):
        self.assertEqual(str(self.event), "Test Event")

# --- TESTS POUR LES VUES ---
class EventViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.thumbnail = SimpleUploadedFile("thumbnail.jpg", b"file_content", content_type="image/jpeg")
        self.banner = SimpleUploadedFile("banner.jpg", b"file_content", content_type="image/jpeg")
        self.event1 = Event.objects.create(
            name="Event 1",
            description="Description 1",
            date=date(2024, 1, 1),
            price_solo=Decimal("10.00"),
            price_duo=Decimal("18.00"),
            price_family=Decimal("25.00"),
            thumbnail=self.thumbnail,
            banner=self.banner
        )
        self.event2 = Event.objects.create(
            name="Event 2",
            description="Description 2",
            date=date(2024, 1, 2),
            price_solo=Decimal("12.00"),
            price_duo=Decimal("20.00"),
            price_family=Decimal("30.00"),
            thumbnail=self.thumbnail,
            banner=self.banner
        )

    def test_event_list_api(self):
        response = self.client.get(reverse("event_list_api"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)  
        self.assertEqual(response.json()[0]["name"], "Event 1")

    def test_all_events_api(self):
        response = self.client.get(reverse("all_events_api"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)  
        self.assertEqual(response.json()[1]["name"], "Event 2")
        
    def test_event_info_view(self):
        response = self.client.get(reverse("eventinfo", args=[self.event1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events/eventinfo.html")
        self.assertContains(response, "Event 1")
        self.assertContains(response, "Description 1")
