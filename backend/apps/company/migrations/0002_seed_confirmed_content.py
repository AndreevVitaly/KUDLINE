from django.db import migrations

def seed_confirmed_content(apps, schema_editor):
    Direction = apps.get_model("company", "Direction")
    ContactInfo = apps.get_model("company", "ContactInfo")
    Direction.objects.get_or_create(
        slug="architectural-metalworks",
        defaults={
            "title": "Архитектурные металлоконструкции и благоустройство",
            "short_description": "Конструкции для общественных пространств: инженерная проработка, изготовление и монтаж.",
            "order": 0,
            "published": True,
        },
    )
    ContactInfo.objects.get_or_create(
        email="kudline@inbox.ru",
        defaults={
            "company_name": "ООО «КУДЛАЙН»",
            "phone": "+7 911 134-26-37",
            "address": "г. Выборг, ул. Промышленная, д. 19",
            "is_active": True,
        },
    )

def unseed(apps, schema_editor):
    apps.get_model("company", "Direction").objects.filter(slug="architectural-metalworks").delete()
    apps.get_model("company", "ContactInfo").objects.filter(email="kudline@inbox.ru").delete()

class Migration(migrations.Migration):
    dependencies = [("company", "0001_initial")]
    operations = [migrations.RunPython(seed_confirmed_content, unseed)]

