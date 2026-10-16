from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Project
from .serializers import ProjectSerializer
class ProjectListView(ListAPIView):
    serializer_class = ProjectSerializer
    def get_queryset(self):
        qs = Project.objects.filter(published=True).prefetch_related("images")
        return qs.filter(featured=True) if self.request.query_params.get("featured") == "true" else qs
class ProjectDetailView(RetrieveAPIView):
    queryset = Project.objects.filter(published=True).prefetch_related("images")
    serializer_class = ProjectSerializer
    lookup_field = "slug"

