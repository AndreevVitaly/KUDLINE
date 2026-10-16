from django.contrib import admin
from .models import ContactInfo, Direction
@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "published")
    list_editable = ("order", "published")
    prepopulated_fields = {"slug": ("title",)}
@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("company_name", "phone", "email", "is_active")

