from django.urls import path
from .views import SiteContentListView
urlpatterns = [path("content/", SiteContentListView.as_view(), name="content-list")]

