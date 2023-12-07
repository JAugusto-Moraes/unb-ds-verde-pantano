# Generated by Django 4.2.5 on 2023-11-26 00:15

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('cnes', models.CharField(default='0000000', editable=False, max_length=7, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('endereco', models.CharField(max_length=150)),
                ('cep', models.CharField(max_length=20)),
                ('categoria', models.CharField(choices=[('HOSPITAL_PUBLICO', 'Público'), ('HOSPITAL_PRIVADO', 'Privado'), ('HOSPITAL_FILANTROPICO', 'Filantrópico')], default='', max_length=100)),
                ('uf', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espirito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'Sâo Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], default='', max_length=100)),
                ('municipio', models.CharField(default='', max_length=150)),
                ('telefone', models.CharField(default='Não informado', max_length=100)),
                ('email', models.CharField(default='Não informado', max_length=100)),
                ('tempo_emergente', models.IntegerField(default=0)),
                ('tempo_muito_urgente', models.IntegerField(default=0)),
                ('tempo_urgente', models.IntegerField(default=0)),
                ('tempo_pouco_urgente', models.IntegerField(default=0)),
                ('tempo_nao_urgente', models.IntegerField(default=0)),
                ('nota', models.DecimalField(decimal_places=3, default=0, max_digits=4)),
                ('leitos', models.IntegerField(default=0)),
                ('uti_adulto', models.IntegerField(default=0)),
                ('uti_pediatrico', models.IntegerField(default=0)),
                ('uti_neonatal', models.IntegerField(default=0)),
                ('uti_queimado', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Hospitais',
            },
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(default='', max_length=100)),
                ('data', models.DateField(default=django.utils.timezone.now)),
                ('atendimento', models.CharField(choices=[('SIM', 'Sim'), ['NAO', 'Não']], default='SIM', max_length=100)),
                ('risco', models.CharField(choices=[('EMERGENTE', 'Emergente'), ('MUITO_URGENTE', 'Muito Urgente'), ('URGENTE', 'Urgente'), ('POUCO_URGENTE', 'Pouco Urgente'), ('NAO_URGENTE', 'Não Urgente')], default='NAO_URGENTE', max_length=100)),
                ('duracao', models.DurationField(default=datetime.timedelta(seconds=1800))),
                ('avaliacao', models.IntegerField(default=3)),
                ('observacao', models.TextField(default='')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicial.hospital')),
            ],
            options={
                'verbose_name': 'avaliação',
                'verbose_name_plural': 'Avaliações',
            },
        ),
    ]
