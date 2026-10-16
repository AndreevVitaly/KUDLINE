from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("company", "0002_seed_confirmed_content")]
    operations = [
        migrations.AddField(
            model_name="direction",
            name="description",
            field=models.TextField(blank=True, verbose_name="Полное описание"),
        ),
    ]
