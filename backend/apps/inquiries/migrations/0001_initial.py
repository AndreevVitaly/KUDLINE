from django.db import migrations, models
import apps.inquiries.models
import apps.inquiries.validators

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(name="Inquiry", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=120, verbose_name="Имя")),
        ("phone", models.CharField(max_length=40, verbose_name="Телефон")), ("email", models.EmailField(blank=True, max_length=254, verbose_name="Email")),
        ("organization", models.CharField(blank=True, max_length=200, verbose_name="Организация")), ("region", models.CharField(blank=True, max_length=160, verbose_name="Город / регион")),
        ("description", models.TextField(verbose_name="Описание задачи")),
        ("attachment", models.FileField(blank=True, upload_to=apps.inquiries.models.inquiry_upload_path, validators=[apps.inquiries.validators.validate_attachment], verbose_name="Вложение")),
        ("status", models.CharField(choices=[("new","Новая"),("in_progress","В работе"),("closed","Закрыта")], default="new", max_length=20, verbose_name="Статус")),
        ("created_at", models.DateTimeField(auto_now_add=True)), ("consent", models.BooleanField(default=False, verbose_name="Согласие на обработку данных")),
    ], options={"verbose_name":"Заявка", "verbose_name_plural":"Заявки", "ordering":("-created_at",)})]

