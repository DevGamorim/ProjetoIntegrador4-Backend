from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    UserStats = (
        (True,'Ativo'),
        (False,'Inativo')
    )

    UserId = models.AutoField(primary_key=True, editable=False, auto_created=True)
    UserFirstName = models.CharField(max_length=255)
    UserLastName = models.CharField(max_length=255)
    UserCPF = models.CharField(max_length=12)
    UserStats = models.BooleanField(choices=UserStats, default=True)
