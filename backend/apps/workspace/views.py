from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import transaction
from django.db.models import Count, Q
from django.middleware.csrf import get_token
from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_protect
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from apps.clients.models import Client, ClientContact, ClientObject, Order, OrderStatusHistory
from apps.inquiries.models import Inquiry
from .models import AuditEvent
from .permissions import IsWorkspaceStaff, WorkspaceModelPermissions
from .serializers import AuditSerializer, ClientSerializer, ContactSerializer, InquirySerializer, ObjectSerializer, OrderSerializer, UserSerializer

def audit(user,obj,operation,changed=None):
    AuditEvent.objects.create(user=user,object_type=obj._meta.label,object_uuid=obj.pk,operation=operation,changed_fields=changed or {})

@api_view(["GET"])
@permission_classes([AllowAny])
def csrf(request): return Response({"csrfToken":get_token(request)})
@api_view(["POST"])
@permission_classes([AllowAny])
@csrf_protect
def sign_in(request):
    user=authenticate(request,username=request.data.get("username"),password=request.data.get("password"))
    if not user or not user.is_staff or not (user.is_superuser or user.groups.filter(name__in=("Администратор","Руководитель","Менеджер")).exists()): return Response({"detail":"Неверные данные или нет доступа."},status=403)
    login(request,user); return Response(UserSerializer(user).data)
@api_view(["POST"])
@permission_classes([IsWorkspaceStaff])
def sign_out(request): logout(request); return Response(status=204)
@api_view(["GET"])
@permission_classes([IsWorkspaceStaff])
def me(request): return Response(UserSerializer(request.user).data)
@api_view(["GET"])
@permission_classes([IsWorkspaceStaff])
def dashboard(request):
    active=Order.objects.exclude(status__in=(Order.Status.COMPLETED,Order.Status.CANCELLED))
    return Response({"new_inquiries":Inquiry.objects.filter(status=Inquiry.Status.NEW).count(),"in_progress_inquiries":Inquiry.objects.filter(status=Inquiry.Status.IN_PROGRESS).count(),"clients":Client.objects.count(),"active_orders":active.count(),"orders_by_status":list(Order.objects.values("status").annotate(count=Count("id"))),"recent_inquiries":InquirySerializer(Inquiry.objects.select_related("client","responsible")[:5],many=True).data,"recent_orders":OrderSerializer(Order.objects.select_related("client","client_object")[:5],many=True).data})
@api_view(["GET"])
@permission_classes([IsWorkspaceStaff])
def users(request): return Response(UserSerializer(get_user_model().objects.filter(is_staff=True,is_active=True).order_by("first_name","username"),many=True).data)

class WorkspacePagination(PageNumberPagination):
    page_size=25; page_size_query_param="page_size"; max_page_size=100
class BaseViewSet(viewsets.ModelViewSet):
    permission_classes=(WorkspaceModelPermissions,); pagination_class=WorkspacePagination; filter_backends=(filters.SearchFilter,filters.OrderingFilter)
    def perform_create(self,s): obj=s.save(); audit(self.request.user,obj,"created")
    def perform_update(self,s):
        fields=list(s.validated_data.keys()); obj=s.save(); audit(self.request.user,obj,"responsible_changed" if "responsible" in fields else "updated",fields)
class ClientViewSet(BaseViewSet):
    queryset=Client.objects.annotate(order_count=Count("orders")).prefetch_related("contacts"); serializer_class=ClientSerializer; search_fields=("display_name","inn","phone","email"); ordering_fields=("display_name","created_at")
    def get_queryset(self):
        q=super().get_queryset(); t=self.request.query_params.get("client_type"); active=self.request.query_params.get("is_active")
        if t:q=q.filter(client_type=t)
        if active in ("true","false"):q=q.filter(is_active=active=="true")
        return q
    @action(detail=False,methods=["get"])
    def duplicates(self,request): return Response(ClientSerializer(self.get_queryset().filter(inn=request.query_params.get("inn","")),many=True).data)
class ObjectViewSet(BaseViewSet):
    queryset=ClientObject.objects.select_related("client"); serializer_class=ObjectSerializer; search_fields=("name","address","city","region","client__display_name")
    def get_queryset(self):
        q=super().get_queryset(); return q.filter(client_id=self.request.query_params["client"]) if self.request.query_params.get("client") else q
class ContactViewSet(BaseViewSet):
    queryset=ClientContact.objects.select_related("client"); serializer_class=ContactSerializer; search_fields=("full_name","phone","email","client__display_name")
    def get_queryset(self):
        q=super().get_queryset(); return q.filter(client_id=self.request.query_params["client"]) if self.request.query_params.get("client") else q
class InquiryViewSet(BaseViewSet):
    queryset=Inquiry.objects.select_related("client","order","responsible"); serializer_class=InquirySerializer; search_fields=("name","organization","phone","email","description"); ordering_fields=("created_at",)
    def get_queryset(self):
        q=super().get_queryset(); return q.filter(status=self.request.query_params["status"]) if self.request.query_params.get("status") else q
    @action(detail=True,methods=["get"])
    def attachment(self,request,pk=None):
        inquiry=self.get_object()
        if not inquiry.attachment: raise Http404
        return FileResponse(inquiry.attachment.open("rb"),as_attachment=True,filename=inquiry.attachment.name.rsplit("/",1)[-1])
    @action(detail=True,methods=["post"])
    @transaction.atomic
    def create_client(self,request,pk=None):
        if not request.user.has_perm("clients.add_client"): raise PermissionDenied("Нет права создавать клиентов.")
        inquiry=self.get_object()
        if inquiry.client_id:return Response({"detail":"Заявка уже связана с клиентом."},status=409)
        data=request.data.copy(); data.setdefault("display_name",inquiry.organization or inquiry.name); data.setdefault("phone",inquiry.phone); data.setdefault("email",inquiry.email); data.setdefault("client_type",Client.Type.LEGAL if inquiry.organization else Client.Type.INDIVIDUAL)
        serializer=ClientSerializer(data=data); serializer.is_valid(raise_exception=True); client=serializer.save(); inquiry.client=client; inquiry.save(update_fields=("client",)); audit(request.user,client,"created_from_inquiry",{"inquiry":str(inquiry.pk)}); audit(request.user,inquiry,"client_linked",{"client":str(client.pk)}); return Response(ClientSerializer(client).data,status=201)
    @action(detail=True,methods=["post"])
    @transaction.atomic
    def link_client(self,request,pk=None):
        inquiry=self.get_object(); client=Client.objects.get(pk=request.data.get("client")); inquiry.client=client; inquiry.save(update_fields=("client",)); audit(request.user,inquiry,"client_linked",{"client":str(client.pk)}); return Response(InquirySerializer(inquiry).data)
class OrderViewSet(BaseViewSet):
    queryset=Order.objects.select_related("client","client_object","responsible").prefetch_related("status_history"); serializer_class=OrderSerializer; search_fields=("number","title","client__display_name"); ordering_fields=("created_at","updated_at","planned_start_date")
    def get_queryset(self):
        q=super().get_queryset();
        if self.request.query_params.get("status"):q=q.filter(status=self.request.query_params["status"])
        if self.request.query_params.get("client"):q=q.filter(client_id=self.request.query_params["client"])
        return q
    @transaction.atomic
    def perform_update(self,s):
        old=s.instance.status; obj=s.save()
        if old!=obj.status: OrderStatusHistory.objects.create(order=obj,previous_status=old,new_status=obj.status,changed_by=self.request.user); audit(self.request.user,obj,"status_changed",{"from":old,"to":obj.status})
        else:audit(self.request.user,obj,"updated",list(s.validated_data.keys()))
class AuditViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=AuditEvent.objects.select_related("user"); serializer_class=AuditSerializer; permission_classes=(WorkspaceModelPermissions,); pagination_class=WorkspacePagination; filter_backends=(filters.SearchFilter,); search_fields=("object_type","operation","user__username")

def deny_private_media(request,path):
    raise Http404
