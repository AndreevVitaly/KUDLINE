from django.test import TestCase
from django.urls import reverse
from .models import Direction

class DirectionApiTests(TestCase):
    def test_only_published_directions_are_returned(self):
        Direction.objects.create(title="Публичное", slug="public", published=True)
        Direction.objects.create(title="Черновик", slug="draft", published=False)
        response = self.client.get("/api/directions/")
        self.assertEqual(response.status_code, 200)
        slugs = {item["slug"] for item in response.json()}
        self.assertIn("public", slugs)
        self.assertNotIn("draft", slugs)

    def test_service_alias_and_detail(self):
        Direction.objects.create(title="Услуга", slug="service", description="Описание", published=True)
        listing = self.client.get("/api/services/")
        detail = self.client.get("/api/services/service/")
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.json()["description"], "Описание")

    def test_contacts_are_public(self):
        response = self.client.get("/api/contacts/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)

