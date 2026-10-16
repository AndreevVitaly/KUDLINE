from django.contrib import admin
from .models import Inquiry
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "organization", "region", "status", "client", "order", "created_at")
    list_filter = ("status", "created_at", "client")
    search_fields = ("name", "phone", "email", "organization", "description")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("client", "order")

