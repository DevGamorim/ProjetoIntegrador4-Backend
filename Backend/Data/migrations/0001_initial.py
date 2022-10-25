# Generated by Django 4.1.1 on 2022-10-18 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Selic',
            fields=[
                ('SlID', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('Slvalue', models.FloatField()),
                ('SlLastUpdate', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('GpId', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('GpName', models.CharField(max_length=255)),
                ('GpStats', models.BooleanField(choices=[(True, 'Ativo'), (False, 'Inativo')])),
                ('GpUse', models.ManyToManyField(related_name='GrupoUsers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Financas',
            fields=[
                ('FinancaID', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('FinancaType', models.BooleanField(choices=[(True, 'Entrada'), (False, 'Saida')])),
                ('FinancaValue', models.FloatField()),
                ('FinancaDateCreate', models.DateTimeField(auto_now_add=True, null=True)),
                ('FinancaDateUpdate', models.DateTimeField(auto_now=True, null=True)),
                ('FinancaStats', models.BooleanField(choices=[(True, 'Ativo'), (False, 'Inativo')])),
                ('FinancaGroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Data.groups')),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('CmID', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('CmMessage', models.CharField(max_length=255)),
                ('CmScore', models.FloatField()),
                ('CmUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Caixas',
            fields=[
                ('CaixaID', models.AutoField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('CaixaTotal', models.FloatField()),
                ('CaixaStats', models.BooleanField(choices=[(True, 'Ativo'), (False, 'Inativo')])),
                ('CaixaFinanca', models.ManyToManyField(to='Data.financas')),
            ],
        ),
    ]
