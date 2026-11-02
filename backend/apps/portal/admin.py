from django.contrib import admin

from .models import ClientDocument, ClientMessage, ClientPortalAccess


@admin.register(ClientPortalAccess)
class ClientPortalAccessAdmin(admin.ModelAdmin):
    list_display = ("user", "client", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("user__username", "user__email", "client__display_name", "client__inn")
    autocomplete_fields = ("user", "client")
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(ClientDocument)
class ClientDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "order", "category", "visible_to_client", "created_at")
    list_filter = ("category", "visible_to_client", "created_at")
    search_fields = ("title", "client__display_name", "order__number")
    autocomplete_fields = ("client", "order", "uploaded_by")
    readonly_fields = ("id", "created_at")

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by_id:
            obj.uploaded_by = request.user
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(ClientMessage)
class ClientMessageAdmin(admin.ModelAdmin):
    list_display = ("client", "direction", "author", "order", "is_read", "created_at")
    list_filter = ("direction", "is_read", "created_at")
    search_fields = ("client__display_name", "body", "order__number", "author__username")
    autocomplete_fields = ("client", "order", "author")
    readonly_fields = ("id", "created_at")

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        if not obj.direction:
            obj.direction = ClientMessage.Direction.STAFF
        obj.full_clean()
        super().save_model(request, obj, form, change)
