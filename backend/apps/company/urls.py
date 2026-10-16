from django.urls import path
from .views import ContactView, DirectionDetailView, DirectionListView
urlpatterns = [
    path("services/", DirectionListView.as_view(), name="service-list"),
    path("services/<slug:slug>/", DirectionDetailView.as_view(), name="service-detail"),
    path("directions/", DirectionListView.as_view(), name="direction-list"),
    path("directions/<slug:slug>/", DirectionDetailView.as_view(), name="direction-detail"),
    path("contacts/", ContactView.as_view(), name="contacts"),
]

