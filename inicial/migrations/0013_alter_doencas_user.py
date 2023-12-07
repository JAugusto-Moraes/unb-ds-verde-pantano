# Generated by Django 4.2.5 on 2023-11-30 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inicial', '0012_doencas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doencas',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doencas', to=settings.AUTH_USER_MODEL),
        ),
    ]
