from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

class WorkspaceModelPermissions(DjangoModelPermissions):
    perms_map = {**DjangoModelPermissions.perms_map, "GET": ["%(app_label)s.view_%(model_name)s"]}
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff) and super().has_permission(request, view)

class IsWorkspaceStaff(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_staff and (request.user.is_superuser or request.user.groups.filter(name__in=("Администратор","Руководитель","Менеджер")).exists())
