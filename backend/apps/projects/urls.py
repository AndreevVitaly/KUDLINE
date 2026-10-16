from django.urls import path
from .views import ProjectDetailView, ProjectListView
urlpatterns = [path("projects/", ProjectListView.as_view()), path("projects/<slug:slug>/", ProjectDetailView.as_view())]

