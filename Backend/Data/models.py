from email.policy import default
from django.db import models
from uuid import uuid4
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Users(AbstractUser):
    UserStats = (
        (True,'Ativo'),
        (False,'Inativo')
    )

    UserFirstName = models.CharField(max_length=255)
    UserLastName = models.CharField(max_length=255)
    UserCPF = models.CharField(max_length=12)
    UserEmail = models.CharField(max_length=255)
    UserStats = models.BooleanField(choices=UserStats)

class Groups(models.Model):
    GpStats = (
        (True,'Ativo'),
        (False,'Inativo')
    )

    GpId = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    GpUse = models.ManyToManyField(Users, related_name="GrupoUsers")
    GpName = models.CharField(max_length=255)
    GpStats = models.BooleanField(choices=GpStats)

class Financas(models.Model):
    FinancaType = (
        (True,'Entrada'),
        (False,'Saida')
    )
    FinancaStats = (
        (True,'Ativo'),
        (False,'Inativo')
    )

    FinancaID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    FinancaGroup = models.ForeignKey(Groups, on_delete=models.CASCADE)
    FinancaType = models.BooleanField(choices=FinancaType)
    FinancaValue = models.FloatField()
    FinancaDateCreate = models.DateTimeField(auto_now_add=True,unique=False, null=True)
    FinancaDateUpdate = models.DateTimeField(auto_now=True,unique=False, null=True)
    FinancaStats = models.BooleanField(choices=FinancaStats)

class Caixas(models.Model):
    CaixaStats = (
        (True,'Ativo'),
        (False,'Inativo')
    )

    CaixaID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    CaixaFinanca = models.ManyToManyField(Financas)
    CaixaTotal = models.FloatField()
    CaixaStats = models.BooleanField(choices=CaixaStats)

#HOgLeGFqrwpZ1rQE