from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import ContactInfo, Direction
from .serializers import ContactInfoSerializer, DirectionSerializer
class DirectionListView(ListAPIView):
    queryset = Direction.objects.filter(published=True)
    serializer_class = DirectionSerializer
class DirectionDetailView(RetrieveAPIView):
    queryset = Direction.objects.filter(published=True)
    serializer_class = DirectionSerializer
    lookup_field = "slug"
class ContactView(ListAPIView):
    queryset = ContactInfo.objects.filter(is_active=True)[:1]
    serializer_class = ContactInfoSerializer

