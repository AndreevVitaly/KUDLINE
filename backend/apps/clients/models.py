import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils import timezone


class Client(models.Model):
    class Type(models.TextChoices):
        LEGAL = "legal", "Юридическое лицо"
        ENTREPRENEUR = "entrepreneur", "Индивидуальный предприниматель"
        INDIVIDUAL = "individual", "Физическое лицо"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_type = models.CharField("Тип клиента", max_length=20, choices=Type.choices)
    display_name = models.CharField("Отображаемое имя", max_length=255, db_index=True)
    full_name = models.CharField("Полное наименование", max_length=500, blank=True)
    short_name = models.CharField("Сокращённое наименование", max_length=255, blank=True)
    inn = models.CharField("ИНН", max_length=12, blank=True, db_index=True)
    kpp = models.CharField("КПП", max_length=9, blank=True)
    ogrn = models.CharField("ОГРН", max_length=15, blank=True)
    ogrnip = models.CharField("ОГРНИП", max_length=15, blank=True)
    phone = models.CharField("Основной телефон", max_length=40, blank=True, db_index=True)
    email = models.EmailField("Основной email", blank=True, db_index=True)
    legal_address = models.TextField("Юридический адрес", blank=True)
    postal_address = models.TextField("Почтовый адрес", blank=True)
    director_name = models.CharField("ФИО руководителя", max_length=255, blank=True)
    director_position = models.CharField("Должность руководителя", max_length=255, blank=True)
    authority_basis = models.CharField("Основание полномочий", max_length=255, blank=True)
    notes = models.TextField("Внутренние заметки", blank=True)
    is_active = models.BooleanField("Активен", default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("display_name",)
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.display_name


class ClientContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="contacts", verbose_name="Клиент")
    full_name = models.CharField("ФИО", max_length=255)
    position = models.CharField("Должность", max_length=255, blank=True)
    phone = models.CharField("Телефон", max_length=40, blank=True)
    email = models.EmailField("Email", blank=True)
    is_primary = models.BooleanField("Основное контактное лицо", default=False)
    notes = models.TextField("Заметки", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-is_primary", "full_name")
        verbose_name = "Контактное лицо"
        verbose_name_plural = "Контактные лица"

    def __str__(self):
        return f"{self.full_name} — {self.client}"


class ClientObject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="client_objects", verbose_name="Клиент")
    name = models.CharField("Название объекта", max_length=255)
    address = models.TextField("Адрес", blank=True)
    city = models.CharField("Город", max_length=160, blank=True)
    region = models.CharField("Регион", max_length=160, blank=True)
    description = models.TextField("Описание", blank=True)
    notes = models.TextField("Внутренние заметки", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("client", "name")
        verbose_name = "Объект клиента"
        verbose_name_plural = "Объекты клиентов"

    def __str__(self):
        return f"{self.name} — {self.client}"


class ClientBankAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="bank_accounts", verbose_name="Клиент")
    account = models.CharField("Расчётный счёт", max_length=20)
    bank_name = models.CharField("Банк", max_length=255)
    bik = models.CharField("БИК", max_length=9)
    correspondent_account = models.CharField("Корреспондентский счёт", max_length=20, blank=True)
    is_primary = models.BooleanField("Основной счёт", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Банковский счёт"
        verbose_name_plural = "Банковские счета"
        constraints = [models.UniqueConstraint(fields=("client", "account"), name="unique_client_bank_account")]

    def __str__(self):
        return f"{self.account} — {self.bank_name}"


class OrderNumberSequence(models.Model):
    year = models.PositiveSmallIntegerField(primary_key=True)
    last_value = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Счётчик номеров заказов"
        verbose_name_plural = "Счётчики номеров заказов"


def generate_order_number():
    year = timezone.localdate().year
    with transaction.atomic():
        sequence, _ = OrderNumberSequence.objects.select_for_update().get_or_create(year=year)
        sequence.last_value += 1
        sequence.save(update_fields=("last_value",))
        return f"KUD-{year}-{sequence.last_value:06d}"


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новый"
        ESTIMATION = "estimation", "Расчёт"
        AGREEMENT = "agreement", "Согласование"
        IN_PRODUCTION = "in_production", "В производстве"
        READY = "ready", "Готов"
        INSTALLATION = "installation", "Монтаж"
        COMPLETED = "completed", "Завершён"
        CANCELLED = "cancelled", "Отменён"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField("Номер заказа", max_length=32, unique=True, editable=False)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="orders", verbose_name="Клиент")
    client_object = models.ForeignKey(ClientObject, on_delete=models.PROTECT, related_name="orders", verbose_name="Объект клиента", blank=True, null=True)
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    status = models.CharField("Статус", max_length=24, choices=Status.choices, default=Status.NEW, db_index=True)
    planned_start_date = models.DateField("Плановое начало", blank=True, null=True)
    planned_end_date = models.DateField("Плановое завершение", blank=True, null=True)
    actual_start_date = models.DateField("Фактическое начало", blank=True, null=True)
    actual_end_date = models.DateField("Фактическое завершение", blank=True, null=True)
    amount = models.DecimalField("Сумма", max_digits=14, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal("0"))])
    currency = models.CharField("Валюта", max_length=3, default="RUB")
    internal_notes = models.TextField("Внутренние заметки", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        constraints = [models.CheckConstraint(condition=models.Q(amount__gte=0) | models.Q(amount__isnull=True), name="order_amount_non_negative")]

    def clean(self):
        super().clean()
        if self.client_object_id and self.client_object.client_id != self.client_id:
            from django.core.exceptions import ValidationError
            raise ValidationError({"client_object": "Объект должен принадлежать выбранному клиенту."})

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} — {self.title}"
