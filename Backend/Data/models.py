from email.policy import default
from django.db import models
from uuid import uuid4
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from users.models import User
# Create your models here.



class Groups(models.Model):
    GpStats = (
        (True,'Ativo'),
        (False,'Inativo')
    )
    GpId = models.AutoField(primary_key=True, editable=False, auto_created=True)
    GpName = models.CharField(max_length=255)
    GpStats = models.BooleanField(choices=GpStats)

class UserGroups(models.Model):
    UsGpId = models.AutoField(primary_key=True, editable=False, auto_created=True)
    GpUse = models.ForeignKey(User, on_delete=models.CASCADE)
    Groups = models.ForeignKey(Groups, on_delete=models.CASCADE)

class Financas(models.Model):
    FinancaType = (
        (True,'Entrada'),
        (False,'Saida')
    )
    FinancaStats = (
        (True,'Ativo'),
        (False,'Inativo')
    )

    FinancaID = models.AutoField(primary_key=True, editable=False, auto_created=True)
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

    CaixaID = models.AutoField(primary_key=True, editable=False, auto_created=True)
    CaixaFinanca = models.ForeignKey(Financas, on_delete=models.CASCADE)
    CaixaTotal = models.FloatField()
    CaixaStats = models.BooleanField(choices=CaixaStats)

class Comentario(models.Model):
    CmID = models.AutoField(primary_key=True, editable=False, auto_created=True)
    CmUser = models.ForeignKey(User, on_delete=models.CASCADE)
    CmMessage = models.CharField(max_length=255)
    CmScore = models.FloatField()

class Selic(models.Model):
    SlID = models.AutoField(primary_key=True, editable=False, auto_created=True)
    Slvalue = models.FloatField()
    SlLastUpdate = models.DateTimeField(null=True)
