# Generated by Django 4.1.1 on 2022-10-02 11:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caixas',
            name='CaixaFinanca',
        ),
        migrations.RemoveField(
            model_name='groups',
            name='GpUse',
        ),
        migrations.AddField(
            model_name='caixas',
            name='CaixaFinanca',
            field=models.ManyToManyField(to='Data.financas'),
        ),
        migrations.AddField(
            model_name='groups',
            name='GpUse',
            field=models.ManyToManyField(related_name='GrupoUsers', to=settings.AUTH_USER_MODEL),
        ),
    ]