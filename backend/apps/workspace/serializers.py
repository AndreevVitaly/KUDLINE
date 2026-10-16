from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.clients.models import Client, ClientContact, ClientObject, Order, OrderStatusHistory
from apps.inquiries.models import Inquiry
from .models import AuditEvent

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta: model=get_user_model(); fields=("id","username","name")
    def get_name(self,obj): return obj.get_full_name() or obj.username

class ContactSerializer(serializers.ModelSerializer):
    class Meta: model=ClientContact; fields="__all__"
class ObjectSerializer(serializers.ModelSerializer):
    client_name=serializers.CharField(source="client.display_name",read_only=True)
    class Meta: model=ClientObject; fields="__all__"
class ClientSerializer(serializers.ModelSerializer):
    order_count=serializers.IntegerField(read_only=True); contacts=ContactSerializer(many=True,read_only=True)
    class Meta: model=Client; fields="__all__"
class InquirySerializer(serializers.ModelSerializer):
    client_name=serializers.CharField(source="client.display_name",read_only=True); responsible_name=serializers.SerializerMethodField()
    class Meta: model=Inquiry; fields="__all__"; read_only_fields=("created_at",)
    def get_responsible_name(self,obj): return (obj.responsible.get_full_name() or obj.responsible.username) if obj.responsible else ""
class StatusHistorySerializer(serializers.ModelSerializer):
    changed_by_name=serializers.CharField(source="changed_by.username",read_only=True)
    class Meta: model=OrderStatusHistory; fields="__all__"
class OrderSerializer(serializers.ModelSerializer):
    client_name=serializers.CharField(source="client.display_name",read_only=True); object_name=serializers.CharField(source="client_object.name",read_only=True); status_history=StatusHistorySerializer(many=True,read_only=True)
    class Meta: model=Order; fields="__all__"; read_only_fields=("number","created_at","updated_at")
    def validate(self,attrs):
        client=attrs.get("client",getattr(self.instance,"client",None)); obj=attrs.get("client_object",getattr(self.instance,"client_object",None))
        if obj and client and obj.client_id != client.id: raise serializers.ValidationError({"client_object":"Объект не принадлежит клиенту."})
        return attrs
class AuditSerializer(serializers.ModelSerializer):
    user_name=serializers.CharField(source="user.username",read_only=True)
    class Meta: model=AuditEvent; fields="__all__"
