from rest_framework import serializers

from apps.clients.models import ClientObject, Order
from .models import ClientDocument, ClientMessage


class PortalOrderSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    object_name = serializers.CharField(source="client_object.name", read_only=True, allow_null=True)

    class Meta:
        model = Order
        fields = ("id", "number", "title", "description", "status", "status_label", "object_name", "planned_start_date", "planned_end_date", "actual_start_date", "actual_end_date", "amount", "currency", "created_at", "updated_at")


class PortalObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientObject
        fields = ("id", "name", "address", "city", "region", "description", "created_at", "updated_at")


class PortalDocumentSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source="get_category_display", read_only=True)
    order_number = serializers.CharField(source="order.number", read_only=True, allow_null=True)
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = ClientDocument
        fields = ("id", "title", "category", "category_label", "order", "order_number", "created_at", "download_url")

    def get_download_url(self, obj):
        return f"/api/client/documents/{obj.pk}/download/"


class PortalMessageSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    order_number = serializers.CharField(source="order.number", read_only=True, allow_null=True)
    attachment_url = serializers.SerializerMethodField()

    class Meta:
        model = ClientMessage
        fields = ("id", "order", "order_number", "direction", "body", "attachment", "attachment_url", "author_name", "is_read", "created_at")
        read_only_fields = ("direction", "is_read", "created_at")
        extra_kwargs = {"attachment": {"write_only": True, "required": False}}

    def get_author_name(self, obj):
        name = obj.author.get_full_name().strip()
        return name or ("Клиент" if obj.direction == ClientMessage.Direction.CLIENT else obj.author.username)

    def get_attachment_url(self, obj):
        return f"/api/client/messages/{obj.pk}/attachment/" if obj.attachment else None

    def validate(self, attrs):
        if not attrs.get("body") and not attrs.get("attachment"):
            raise serializers.ValidationError("Добавьте текст сообщения или файл.")
        order = attrs.get("order")
        client = self.context["request"].user.client_portal_access.client
        if order and order.client_id != client.id:
            raise serializers.ValidationError({"order": "Этот заказ недоступен."})
        return attrs
