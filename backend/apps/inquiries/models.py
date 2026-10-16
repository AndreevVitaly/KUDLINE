import uuid
from datetime import date
from pathlib import Path
from django.db import models
from .validators import validate_attachment

def inquiry_upload_path(instance, filename):
    suffix = Path(filename).suffix.lower()
    today = date.today()
    return f"inquiries/{today:%Y/%m}/{uuid.uuid4().hex}{suffix}"

class Inquiry(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_PROGRESS = "in_progress", "В работе"
        CLOSED = "closed", "Закрыта"
    name = models.CharField("Имя", max_length=120)
    phone = models.CharField("Телефон", max_length=40)
    email = models.EmailField("Email", blank=True)
    organization = models.CharField("Организация", max_length=200, blank=True)
    region = models.CharField("Город / регион", max_length=160, blank=True)
    description = models.TextField("Описание задачи")
    attachment = models.FileField("Вложение", upload_to=inquiry_upload_path, validators=[validate_attachment], blank=True)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    consent = models.BooleanField("Согласие на обработку данных", default=False)
    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
    def __str__(self): return f"{self.name} — {self.created_at:%d.%m.%Y}"

