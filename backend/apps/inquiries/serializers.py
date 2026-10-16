from rest_framework import serializers
from .models import Inquiry
class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ("id", "name", "phone", "email", "organization", "region", "description", "attachment", "consent", "created_at")
        read_only_fields = ("id", "created_at")
    def validate_consent(self, value):
        if not value: raise serializers.ValidationError("Необходимо согласие на обработку персональных данных.")
        return value

