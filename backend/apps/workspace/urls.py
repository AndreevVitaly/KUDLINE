from django.urls import include,path
from rest_framework.routers import DefaultRouter
from . import views
router=DefaultRouter(); router.register("inquiries",views.InquiryViewSet); router.register("clients",views.ClientViewSet); router.register("contacts",views.ContactViewSet); router.register("objects",views.ObjectViewSet); router.register("orders",views.OrderViewSet); router.register("audit",views.AuditViewSet)
urlpatterns=[path("auth/csrf/",views.csrf),path("auth/login/",views.sign_in),path("auth/logout/",views.sign_out),path("auth/me/",views.me),path("dashboard/",views.dashboard),path("users/",views.users),path("",include(router.urls))]
