from rest_framework.generics import ListAPIView
from .models import SiteContent
from .serializers import SiteContentSerializer
class SiteContentListView(ListAPIView):
    queryset = SiteContent.objects.all().order_by("key")
    serializer_class = SiteContentSerializer

