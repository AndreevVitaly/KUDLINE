from django.contrib import admin
from .models import AuditEvent

@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display=("created_at","user","operation","object_type","object_uuid")
    list_filter=("operation","object_type","created_at")
    search_fields=("user__username","object_type","object_uuid")
    readonly_fields=("id","object_type","object_uuid","operation","user","changed_fields","created_at")
    def has_add_permission(self,request): return False
    def has_change_permission(self,request,obj=None): return False
    def has_delete_permission(self,request,obj=None): return False
