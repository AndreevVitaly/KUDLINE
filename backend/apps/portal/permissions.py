from rest_framework.permissions import BasePermission


class IsClientPortalUser(BasePermission):
    message = "Нет доступа к личному кабинету клиента."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            access = request.user.client_portal_access
        except AttributeError:
            return False
        return access.is_active and access.client.is_active
