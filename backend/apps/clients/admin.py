from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from .models import Client, ClientBankAccount, ClientContact, ClientObject, Order, OrderNumberSequence


class ClientContactInline(admin.TabularInline):
    model = ClientContact
    extra = 0
    fields = ("full_name", "position", "phone", "email", "is_primary")


class ClientObjectInline(admin.TabularInline):
    model = ClientObject
    extra = 0
    fields = ("name", "city", "region", "address")


class ClientBankAccountInline(admin.TabularInline):
    model = ClientBankAccount
    extra = 0
    fields = ("account", "bank_name", "bik", "is_primary")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("display_name", "client_type", "inn", "phone", "email", "is_active", "updated_at")
    list_filter = ("client_type", "is_active", "created_at")
    search_fields = ("display_name", "full_name", "short_name", "inn", "phone", "email")
    readonly_fields = ("id", "created_at", "updated_at", "related_inquiries", "related_orders")
    inlines = (ClientContactInline, ClientObjectInline, ClientBankAccountInline)
    fieldsets = (
        ("Клиент", {"fields": ("id", "client_type", "display_name", "full_name", "short_name", "is_active")}),
        ("Реквизиты", {"fields": ("inn", "kpp", "ogrn", "ogrnip", "legal_address", "postal_address")}),
        ("Контакты", {"fields": ("phone", "email")}),
        ("Руководитель", {"fields": ("director_name", "director_position", "authority_basis"), "classes": ("collapse",)}),
        ("История", {"fields": ("related_inquiries", "related_orders", "notes", "created_at", "updated_at")}),
    )

    def save_model(self, request, obj, form, change):
        if obj.inn:
            duplicates = Client.objects.filter(inn=obj.inn).exclude(pk=obj.pk)
            if duplicates.exists():
                names = ", ".join(duplicates.values_list("display_name", flat=True)[:5])
                self.message_user(request, f"Внимание: клиент с ИНН {obj.inn} уже существует: {names}", level=messages.WARNING)
        super().save_model(request, obj, form, change)

    @admin.display(description="Связанные заявки")
    def related_inquiries(self, obj):
        return format_html_join("", '<a href="{}">{} — {}</a><br>', (
            (reverse("admin:inquiries_inquiry_change", args=(item.pk,)), item.name, item.created_at.strftime("%d.%m.%Y"))
            for item in obj.inquiries.all()[:20]
        )) or "—"

    @admin.display(description="Связанные заказы")
    def related_orders(self, obj):
        return format_html_join("", '<a href="{}">{} — {}</a><br>', (
            (reverse("admin:clients_order_change", args=(item.pk,)), item.number, item.title)
            for item in obj.orders.all()[:20]
        )) or "—"


@admin.register(ClientContact)
class ClientContactAdmin(admin.ModelAdmin):
    list_display = ("full_name", "client", "position", "phone", "email", "is_primary")
    list_filter = ("is_primary",)
    search_fields = ("full_name", "client__display_name", "phone", "email")
    autocomplete_fields = ("client",)


@admin.register(ClientObject)
class ClientObjectAdmin(admin.ModelAdmin):
    list_display = ("name", "client", "city", "region", "updated_at")
    search_fields = ("name", "client__display_name", "address", "city", "region")
    autocomplete_fields = ("client",)


@admin.register(ClientBankAccount)
class ClientBankAccountAdmin(admin.ModelAdmin):
    list_display = ("account", "client", "bank_name", "bik", "is_primary")
    search_fields = ("account", "client__display_name", "bank_name", "bik")
    autocomplete_fields = ("client",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "client", "status", "amount", "currency", "created_at")
    list_filter = ("status", "created_at", "planned_start_date", "planned_end_date")
    search_fields = ("number", "title", "client__display_name", "client__inn")
    autocomplete_fields = ("client", "client_object")
    readonly_fields = ("id", "number", "created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(OrderNumberSequence)
class OrderNumberSequenceAdmin(admin.ModelAdmin):
    list_display = ("year", "last_value")
    readonly_fields = ("year", "last_value")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
