from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from apps.inquiries.models import Inquiry
from .models import Client, ClientContact, ClientObject, Order


class ClientModelTests(TestCase):
    def test_creates_legal_client_and_contact(self):
        client = Client.objects.create(client_type=Client.Type.LEGAL, display_name='ООО "Тест"', inn="1234567890")
        contact = ClientContact.objects.create(client=client, full_name="Иван Иванов", is_primary=True)
        self.assertEqual(contact.client, client)

    def test_creates_individual_without_company_details(self):
        client = Client.objects.create(client_type=Client.Type.INDIVIDUAL, display_name="Иван Иванов")
        self.assertEqual(client.inn, "")

    def test_client_object_belongs_to_client(self):
        client = Client.objects.create(client_type=Client.Type.LEGAL, display_name="Заказчик")
        client_object = ClientObject.objects.create(client=client, name="Производственный корпус")
        self.assertEqual(client_object.client, client)


class OrderModelTests(TestCase):
    def setUp(self):
        self.client_record = Client.objects.create(client_type=Client.Type.LEGAL, display_name="Заказчик")
        self.client_object = ClientObject.objects.create(client=self.client_record, name="Объект")

    def test_creates_order_with_human_number_and_relations(self):
        order = Order.objects.create(client=self.client_record, client_object=self.client_object, title="Металлоконструкции", amount=Decimal("1000.00"))
        self.assertRegex(order.number, r"^KUD-\d{4}-\d{6}$")
        self.assertEqual(order.status, Order.Status.NEW)

    def test_order_number_is_unique(self):
        first = Order.objects.create(client=self.client_record, title="Первый")
        second = Order.objects.create(client=self.client_record, title="Второй")
        self.assertNotEqual(first.number, second.number)

    def test_rejects_object_of_another_client(self):
        other = Client.objects.create(client_type=Client.Type.LEGAL, display_name="Другой")
        order = Order(client=other, client_object=self.client_object, title="Ошибка")
        with self.assertRaises(ValidationError):
            order.full_clean()

    def test_database_rejects_negative_amount(self):
        with self.assertRaises(IntegrityError):
            Order.objects.create(client=self.client_record, title="Ошибка", amount=Decimal("-1"))


class InquiryRelationsAndSecurityTests(TestCase):
    def test_inquiry_can_link_to_client_and_order(self):
        client = Client.objects.create(client_type=Client.Type.LEGAL, display_name="Заказчик")
        order = Order.objects.create(client=client, title="Заказ")
        inquiry = Inquiry.objects.create(name="Контакт", phone="+7 900 000-00-00", description="Заявка", consent=True, client=client, order=order)
        self.assertEqual(inquiry.client, client)
        self.assertEqual(inquiry.order, order)

    def test_old_inquiry_does_not_require_relations(self):
        inquiry = Inquiry.objects.create(name="Контакт", phone="123", description="Заявка", consent=True)
        self.assertIsNone(inquiry.client)
        self.assertIsNone(inquiry.order)

    def test_private_models_have_no_public_api(self):
        self.assertEqual(self.client.get("/api/clients/").status_code, 404)
        self.assertEqual(self.client.get("/api/orders/").status_code, 404)
