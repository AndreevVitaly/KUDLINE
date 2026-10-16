from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(name="SiteContent", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("key", models.SlugField(unique=True, verbose_name="Ключ")),
        ("title", models.CharField(blank=True, max_length=200, verbose_name="Заголовок")),
        ("body", models.TextField(blank=True, verbose_name="Текст")),
        ("image", models.ImageField(blank=True, upload_to="content/", verbose_name="Изображение")),
        ("updated_at", models.DateTimeField(auto_now=True)),
    ], options={"verbose_name":"Информационный блок", "verbose_name_plural":"Информационные блоки"})]

