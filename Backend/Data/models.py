from email.policy import default
from django.db import models
from uuid import uuid4
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Users(AbstractUser):
    UserFirstName = models.CharField(max_length=255)
    UserLastName = models.CharField(max_length=255)
    UserCPF = models.CharField(max_length=12)
    UserEmail = models.CharField(max_length=255)

class Financas(models.Model):
    FinancaType = (
        (True,'Entrada'),
        (False,'Saida')
    )

    FinancaID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    FinancaUser = models.ForeignKey(Users, on_delete=models.CASCADE)
    FinancaType = models.BooleanField(choices=FinancaType)
    FinancaValue = models.FloatField()
    FinancaDateCreate = models.DateTimeField(auto_now_add=True,unique=False, null=True)
    FinancaDateUpdate = models.DateTimeField(auto_now=True,unique=False, null=True)
    
class Groups(models.Model):
    GroupID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    GroupName = models.CharField(max_length=255)

class Caixas(models.Model):
    CaixaID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    CaixaGroup = models.ForeignKey(Groups, on_delete=models.CASCADE)
    CaixaFinanca = models.ForeignKey(Financas, on_delete=models.CASCADE)
    CaixaTotal = models.FloatField()

#HOgLeGFqrwpZ1rQE