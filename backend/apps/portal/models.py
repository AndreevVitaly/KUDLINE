import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.clients.models import Client, Order


class ClientPortalAccess(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="client_portal_access", verbose_name="Пользователь")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="portal_accesses", verbose_name="Клиент")
    is_active = models.BooleanField("Доступ активен", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Доступ в кабинет"
        verbose_name_plural = "Доступы в кабинет"

    def __str__(self):
        return f"{self.user} — {self.client}"


class ClientDocument(models.Model):
    class Category(models.TextChoices):
        CONTRACT = "contract", "Договор"
        INVOICE = "invoice", "Счёт"
        ACT = "act", "Акт"
        DRAWING = "drawing", "Чертёж"
        OTHER = "other", "Другое"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="portal_documents", verbose_name="Клиент")
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="portal_documents", verbose_name="Заказ", blank=True, null=True)
    title = models.CharField("Название", max_length=255)
    category = models.CharField("Категория", max_length=20, choices=Category.choices, default=Category.OTHER)
    file = models.FileField("Файл", upload_to="client_portal/documents/%Y/%m/")
    visible_to_client = models.BooleanField("Доступен клиенту", default=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="uploaded_client_documents", verbose_name="Загрузил", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Документ клиента"
        verbose_name_plural = "Документы клиентов"

    def clean(self):
        if self.order_id and self.order.client_id != self.client_id:
            raise ValidationError({"order": "Заказ должен принадлежать выбранному клиенту."})

    def __str__(self):
        return self.title


class ClientMessage(models.Model):
    class Direction(models.TextChoices):
        CLIENT = "client", "От клиента"
        STAFF = "staff", "От сотрудника"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="portal_messages", verbose_name="Клиент")
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="portal_messages", verbose_name="Заказ", blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="client_portal_messages", verbose_name="Автор")
    direction = models.CharField("Направление", max_length=12, choices=Direction.choices)
    body = models.TextField("Сообщение", blank=True)
    attachment = models.FileField("Вложение", upload_to="client_portal/messages/%Y/%m/", blank=True)
    is_read = models.BooleanField("Прочитано", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "Сообщение клиента"
        verbose_name_plural = "Сообщения клиентов"

    def clean(self):
        if not self.body and not self.attachment:
            raise ValidationError("Добавьте текст или файл.")
        if self.order_id and self.order.client_id != self.client_id:
            raise ValidationError({"order": "Заказ должен принадлежать выбранному клиенту."})

    def __str__(self):
        return f"{self.client} — {self.get_direction_display()}"
