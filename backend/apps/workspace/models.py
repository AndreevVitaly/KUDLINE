import uuid
from django.conf import settings
from django.db import models

class AuditEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    object_type = models.CharField(max_length=60, db_index=True)
    object_uuid = models.UUIDField(db_index=True)
    operation = models.CharField(max_length=60, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="kudline_audit_events")
    changed_fields = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Событие аудита"
        verbose_name_plural = "Журнал действий"
