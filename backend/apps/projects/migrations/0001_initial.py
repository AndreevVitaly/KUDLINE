from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Project", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("title", models.CharField(max_length=240, verbose_name="Название")),
            ("slug", models.SlugField(unique=True)), ("short_description", models.TextField(blank=True, verbose_name="Краткое описание")),
            ("description", models.TextField(blank=True, verbose_name="Описание задачи")), ("completed_work", models.TextField(blank=True, verbose_name="Выполненные работы")),
            ("features", models.TextField(blank=True, verbose_name="Особенности конструкции")), ("result", models.TextField(blank=True, verbose_name="Результат")),
            ("location", models.CharField(blank=True, max_length=200, verbose_name="Местоположение")), ("year", models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Год")),
            ("cover_image", models.ImageField(blank=True, upload_to="projects/covers/", verbose_name="Обложка")), ("published", models.BooleanField(default=False, verbose_name="Опубликовано")),
            ("featured", models.BooleanField(default=False, verbose_name="На главной")), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
        ], options={"verbose_name":"Проект", "verbose_name_plural":"Проекты", "ordering":("-year","-created_at")}),
        migrations.CreateModel(name="ProjectImage", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("image", models.ImageField(upload_to="projects/gallery/", verbose_name="Фотография")),
            ("caption", models.CharField(blank=True, max_length=240, verbose_name="Подпись")), ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
            ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="projects.project")),
        ], options={"verbose_name":"Фотография проекта", "verbose_name_plural":"Фотографии проектов", "ordering":("order","id")}),
    ]

