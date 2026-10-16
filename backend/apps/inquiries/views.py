from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from .models import Inquiry
from .serializers import InquirySerializer
class InquiryCreateView(CreateAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

