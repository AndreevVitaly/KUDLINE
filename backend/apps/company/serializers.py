from rest_framework import serializers
from .models import ContactInfo, Direction
class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ("title", "slug", "short_description", "description", "image", "order")
class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ("company_name", "phone", "email", "address", "requisites")

