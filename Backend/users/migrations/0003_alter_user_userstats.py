# Generated by Django 4.1.1 on 2022-10-02 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_useremail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='UserStats',
            field=models.BooleanField(choices=[(True, 'Ativo'), (False, 'Inativo')], default=True),
        ),
    ]