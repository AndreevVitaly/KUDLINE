from pathlib import Path

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import Count
from django.http import FileResponse, Http404
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.clients.models import Client, ClientObject, Order
from .models import ClientDocument, ClientMessage, ClientPortalAccess
from .permissions import IsClientPortalUser
from .serializers import PortalDocumentSerializer, PortalMessageSerializer, PortalObjectSerializer, PortalOrderSerializer


def portal_access(user):
    try:
        access = user.client_portal_access
    except AttributeError:
        return None
    return access if access.is_active and access.client.is_active else None


def validate_upload(upload):
    if not upload:
        return None
    if upload.size > 10 * 1024 * 1024:
        return "Размер файла не должен превышать 10 МБ."
    allowed = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".doc", ".docx", ".xls", ".xlsx", ".zip"}
    if Path(upload.name).suffix.lower() not in allowed:
        return "Допустимы PDF, изображения, документы Office и ZIP."
    return None


@api_view(["GET"])
@permission_classes([AllowAny])
def csrf(request):
    return Response({"csrfToken": get_token(request)})


@api_view(["POST"])
@permission_classes([AllowAny])
@csrf_protect
def register(request):
    name = str(request.data.get("name", "")).strip()
    email = str(request.data.get("email", "")).strip().lower()
    password = str(request.data.get("password", ""))
    password_confirm = str(request.data.get("password_confirm", ""))
    errors = {}
    if len(name) < 2 or len(name) > 150:
        errors["name"] = "Имя для входа должно содержать от 2 до 150 символов."
    else:
        try:
            UnicodeUsernameValidator()(name)
        except ValidationError:
            errors["name"] = "Используйте буквы, цифры и символы @ . + - _."
    try:
        validate_email(email)
    except ValidationError:
        errors["email"] = "Введите корректный email."
    if len(password) < 8:
        errors["password"] = "Пароль должен содержать не менее 8 символов."
    if password != password_confirm:
        errors["password_confirm"] = "Пароли не совпадают."
    User = get_user_model()
    if name and User.objects.filter(username__iexact=name).exists():
        errors["name"] = "Это имя уже занято."
    if email and User.objects.filter(email__iexact=email).exists():
        errors["email"] = "Пользователь с таким email уже зарегистрирован."
    if errors:
        return Response({"detail": "Проверьте данные формы.", "errors": errors}, status=400)
    with transaction.atomic():
        user = User.objects.create_user(username=name, email=email, password=password, first_name=name)
        client = Client.objects.create(client_type=Client.Type.INDIVIDUAL, display_name=name, email=email, notes="Создано через саморегистрацию личного кабинета.")
        ClientPortalAccess.objects.create(user=user, client=client)
    return Response({"detail": "Регистрация завершена. Теперь войдите по имени и паролю."}, status=201)


@api_view(["POST"])
@permission_classes([AllowAny])
@csrf_protect
def sign_in(request):
    user = authenticate(request, username=request.data.get("username"), password=request.data.get("password"))
    access = portal_access(user) if user else None
    if not access:
        return Response({"detail": "Неверные данные или доступ в кабинет не предоставлен."}, status=403)
    login(request, user)
    return Response({"username": user.username, "name": user.get_full_name() or user.username, "client": {"id": access.client_id, "name": access.client.display_name}})


@api_view(["POST"])
@permission_classes([IsClientPortalUser])
def sign_out(request):
    logout(request)
    return Response(status=204)


@api_view(["GET"])
@permission_classes([IsClientPortalUser])
def me(request):
    access = request.user.client_portal_access
    return Response({"username": request.user.username, "name": request.user.get_full_name() or request.user.username, "client": {"id": access.client_id, "name": access.client.display_name}})


@api_view(["GET"])
@permission_classes([IsClientPortalUser])
def dashboard(request):
    client = request.user.client_portal_access.client
    orders = Order.objects.filter(client=client).select_related("client_object")
    active = orders.exclude(status__in=(Order.Status.COMPLETED, Order.Status.CANCELLED))
    return Response({
        "client": {"name": client.display_name, "inn": client.inn, "phone": client.phone, "email": client.email},
        "active_orders": active.count(),
        "objects": ClientObject.objects.filter(client=client).count(),
        "documents": ClientDocument.objects.filter(client=client, visible_to_client=True).count(),
        "unread_messages": ClientMessage.objects.filter(client=client, direction=ClientMessage.Direction.STAFF, is_read=False).count(),
        "orders_by_status": list(orders.values("status").annotate(count=Count("id"))),
        "recent_orders": PortalOrderSerializer(orders[:5], many=True).data,
    })


@api_view(["GET"])
@permission_classes([IsClientPortalUser])
def orders(request):
    queryset = Order.objects.filter(client=request.user.client_portal_access.client).select_related("client_object")
    return Response(PortalOrderSerializer(queryset, many=True).data)


@api_view(["GET"])
@permission_classes([IsClientPortalUser])
def order_detail(request, pk):
    obj = get_object_or_404(Order.objects.select_related("client_object"), pk=pk, client=request.user.client_portal_access.client)
    return Response(PortalOrderSerializer(obj).data)


@api_view(["GET"])
@permission_classes([IsClientPortalUser])
def objects(request):
    queryset = ClientObject.objects.filter(client=request.user.client_portal_access.client)
    return Response(PortalObjectSerializer(queryset, many=True).data)


@api_view(["GET"])
@permission_classes([IsClientPortalUser])
def documents(request):
    queryset = ClientDocument.objects.filter(client=request.user.client_portal_access.client, visible_to_client=True).select_related("order")
    return Response(PortalDocumentSerializer(queryset, many=True).data)


@api_view(["GET"])
@permission_classes([IsClientPortalUser])
def document_download(request, pk):
    obj = get_object_or_404(ClientDocument, pk=pk, client=request.user.client_portal_access.client, visible_to_client=True)
    if not obj.file:
        raise Http404
    return FileResponse(obj.file.open("rb"), as_attachment=True, filename=Path(obj.file.name).name)


@api_view(["GET", "POST"])
@permission_classes([IsClientPortalUser])
def messages(request):
    client = request.user.client_portal_access.client
    if request.method == "GET":
        ClientMessage.objects.filter(client=client, direction=ClientMessage.Direction.STAFF, is_read=False).update(is_read=True)
        queryset = ClientMessage.objects.filter(client=client).select_related("author", "order")
        return Response(PortalMessageSerializer(queryset, many=True).data)
    upload_error = validate_upload(request.FILES.get("attachment"))
    if upload_error:
        return Response({"detail": upload_error}, status=400)
    serializer = PortalMessageSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save(client=client, author=request.user, direction=ClientMessage.Direction.CLIENT)
    return Response(serializer.data, status=201)


@api_view(["GET"])
@permission_classes([IsClientPortalUser])
def message_attachment(request, pk):
    obj = get_object_or_404(ClientMessage, pk=pk, client=request.user.client_portal_access.client)
    if not obj.attachment:
        raise Http404
    return FileResponse(obj.attachment.open("rb"), as_attachment=True, filename=Path(obj.attachment.name).name)


def deny_private_media(request, path):
    raise Http404
