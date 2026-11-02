from django.urls import path

from . import views

urlpatterns = [
    path("auth/csrf/", views.csrf),
    path("auth/register/", views.register),
    path("auth/login/", views.sign_in),
    path("auth/logout/", views.sign_out),
    path("auth/me/", views.me),
    path("dashboard/", views.dashboard),
    path("orders/", views.orders),
    path("orders/<uuid:pk>/", views.order_detail),
    path("objects/", views.objects),
    path("documents/", views.documents),
    path("documents/<uuid:pk>/download/", views.document_download),
    path("messages/", views.messages),
    path("messages/<uuid:pk>/attachment/", views.message_attachment),
]
