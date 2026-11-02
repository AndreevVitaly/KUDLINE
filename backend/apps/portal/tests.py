import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.clients.models import Client, ClientObject, Order
from .models import ClientDocument, ClientMessage, ClientPortalAccess


class ClientPortalTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._media_root = tempfile.mkdtemp()
        cls._media_override = override_settings(MEDIA_ROOT=cls._media_root)
        cls._media_override.enable()

    @classmethod
    def tearDownClass(cls):
        cls._media_override.disable()
        shutil.rmtree(cls._media_root, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user("client-user", password="strong-test-password")
        self.other_user = User.objects.create_user("other-client", password="strong-test-password")
        self.client_record = Client.objects.create(client_type=Client.Type.LEGAL, display_name="ООО Клиент")
        self.other_client = Client.objects.create(client_type=Client.Type.LEGAL, display_name="ООО Другой")
        ClientPortalAccess.objects.create(user=self.user, client=self.client_record)
        ClientPortalAccess.objects.create(user=self.other_user, client=self.other_client)
        self.order = Order.objects.create(client=self.client_record, title="Свой заказ")
        self.other_order = Order.objects.create(client=self.other_client, title="Чужой заказ")
        ClientObject.objects.create(client=self.client_record, name="Свой объект")
        ClientObject.objects.create(client=self.other_client, name="Чужой объект")
        self.document = ClientDocument.objects.create(client=self.client_record, order=self.order, title="Договор", file=SimpleUploadedFile("contract.pdf", b"test", content_type="application/pdf"))
        self.other_document = ClientDocument.objects.create(client=self.other_client, order=self.other_order, title="Чужой договор", file=SimpleUploadedFile("other.pdf", b"test", content_type="application/pdf"))
        self.api = APIClient()

    def test_anonymous_user_cannot_access_portal(self):
        self.assertIn(self.api.get("/api/client/dashboard/").status_code, (401, 403))

    def test_client_login_and_me(self):
        response = self.api.post("/api/client/auth/login/", {"username": "client-user", "password": "strong-test-password"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.api.get("/api/client/auth/me/").data["client"]["name"], "ООО Клиент")

    def test_client_can_register_and_then_login_by_name(self):
        response = self.api.post("/api/client/auth/register/", {"name": "Иван", "email": "ivan.personal@example.com", "password": "secure-pass-123", "password_confirm": "secure-pass-123"}, format="json")
        self.assertEqual(response.status_code, 201)
        User = get_user_model()
        user = User.objects.get(username="Иван")
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, "ivan.personal@example.com")
        self.assertEqual(user.client_portal_access.client.display_name, "Иван")
        login_response = self.api.post("/api/client/auth/login/", {"username": "Иван", "password": "secure-pass-123"}, format="json")
        self.assertEqual(login_response.status_code, 200)

    def test_registration_rejects_duplicate_email_and_short_password(self):
        first = self.api.post("/api/client/auth/register/", {"name": "Мария", "email": "unique@example.com", "password": "secure-pass-123", "password_confirm": "secure-pass-123"}, format="json")
        self.assertEqual(first.status_code, 201)
        duplicate = self.api.post("/api/client/auth/register/", {"name": "Ольга", "email": "UNIQUE@example.com", "password": "short", "password_confirm": "short"}, format="json")
        self.assertEqual(duplicate.status_code, 400)
        self.assertIn("email", duplicate.data["errors"])
        self.assertIn("password", duplicate.data["errors"])

    def test_client_sees_only_own_orders_objects_and_documents(self):
        self.api.force_authenticate(self.user)
        self.assertEqual([item["title"] for item in self.api.get("/api/client/orders/").data], ["Свой заказ"])
        self.assertEqual([item["name"] for item in self.api.get("/api/client/objects/").data], ["Свой объект"])
        self.assertEqual([item["title"] for item in self.api.get("/api/client/documents/").data], ["Договор"])
        self.assertEqual(self.api.get(f"/api/client/orders/{self.other_order.pk}/").status_code, 404)
        self.assertEqual(self.api.get(f"/api/client/documents/{self.other_document.pk}/download/").status_code, 404)

    def test_client_message_is_bound_to_client(self):
        self.api.force_authenticate(self.user)
        response = self.api.post("/api/client/messages/", {"body": "Нужна консультация", "order": str(self.order.pk)}, format="json")
        self.assertEqual(response.status_code, 201)
        message = ClientMessage.objects.get()
        self.assertEqual(message.client, self.client_record)
        self.assertEqual(message.author, self.user)
        self.assertEqual(message.direction, ClientMessage.Direction.CLIENT)
        denied = self.api.post("/api/client/messages/", {"body": "Ошибка", "order": str(self.other_order.pk)}, format="json")
        self.assertEqual(denied.status_code, 400)

    def test_private_media_is_not_served_directly(self):
        self.assertEqual(self.client.get("/media/client_portal/documents/secret.pdf").status_code, 404)
