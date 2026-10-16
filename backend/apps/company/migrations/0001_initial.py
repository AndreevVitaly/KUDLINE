from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="ContactInfo", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("company_name", models.CharField(default="ООО «КУДЛАЙН»", max_length=200, verbose_name="Компания")),
            ("phone", models.CharField(max_length=50, verbose_name="Телефон")), ("email", models.EmailField(max_length=254, verbose_name="Email")),
            ("address", models.CharField(max_length=300, verbose_name="Адрес производства")), ("requisites", models.TextField(blank=True, verbose_name="Реквизиты")),
            ("is_active", models.BooleanField(default=True, verbose_name="Активно")),
        ], options={"verbose_name":"Контактные данные", "verbose_name_plural":"Контактные данные"}),
        migrations.CreateModel(name="Direction", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=200, verbose_name="Название")), ("slug", models.SlugField(unique=True)),
            ("short_description", models.TextField(blank=True, verbose_name="Краткое описание")), ("image", models.ImageField(blank=True, upload_to="directions/", verbose_name="Изображение")),
            ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок")), ("published", models.BooleanField(default=True, verbose_name="Опубликовано")),
        ], options={"verbose_name":"Направление", "verbose_name_plural":"Направления", "ordering":("order","title")}),
    ]

