# Generated by Django 4.2.5 on 2023-11-30 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inicial', '0011_alter_dados_exercicio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doencas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doenca', models.CharField(default='N/A', max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'doença',
                'verbose_name_plural': 'Doenças',
            },
        ),
    ]
