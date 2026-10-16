from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from rest_framework.test import APIClient
from apps.clients.models import Client,Order,OrderStatusHistory
from .models import AuditEvent

class WorkspaceSecurityTests(TestCase):
    def setUp(self):
        self.api=APIClient(); self.user=get_user_model().objects.create_user("manager",password="safe-test-password",is_staff=True)
        self.user.user_permissions.set(Permission.objects.filter(content_type__app_label__in=("clients","inquiries","workspace")))
    def test_anonymous_cannot_access_internal_data(self): self.assertIn(self.api.get("/api/internal/clients/").status_code,(401,403))
    def test_non_staff_cannot_access_workspace(self):
        user=get_user_model().objects.create_user("public",password="safe-test-password");self.api.force_authenticate(user);self.assertEqual(self.api.get("/api/internal/dashboard/").status_code,403)
    def test_manager_creates_client_and_audit_event(self):
        self.api.force_authenticate(self.user);r=self.api.post("/api/internal/clients/",{"display_name":"Тест","client_type":"legal"},format="json");self.assertEqual(r.status_code,201);self.assertTrue(AuditEvent.objects.filter(operation="created",object_uuid=r.data["id"]).exists())
    def test_status_change_has_history(self):
        client=Client.objects.create(display_name="Тест",client_type="legal");order=Order.objects.create(client=client,title="Заказ");self.api.force_authenticate(self.user);r=self.api.patch(f"/api/internal/orders/{order.pk}/",{"status":"estimation"},format="json");self.assertEqual(r.status_code,200);self.assertTrue(OrderStatusHistory.objects.filter(order=order,new_status="estimation",changed_by=self.user).exists())
    def test_public_site_still_available(self): self.assertEqual(self.client.get("/api/services/").status_code,200)
