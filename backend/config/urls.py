from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from apps.workspace.views import deny_private_media
from apps.portal.views import deny_private_media as deny_client_portal_media

urlpatterns = [
    path("media/inquiries/<path:path>", deny_private_media),
    path("media/client_portal/<path:path>", deny_client_portal_media),
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
    path("api/", include("apps.company.urls")),
    path("api/", include("apps.projects.urls")),
    path("api/", include("apps.inquiries.urls")),
    path("api/internal/", include("apps.workspace.urls")),
    path("api/client/", include("apps.portal.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

