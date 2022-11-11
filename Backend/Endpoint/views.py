from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
# Create your views here.

from Data.models import Financas, Groups, Caixas, Comentario, Selic, UserGroups
from users.models import User

# libs import
import requests
from datetime import datetime
import json


url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json&dataInicial=18/10/2022&dataFinal=18/10/2022"
response = requests.request("GET", url)
response = response.text.encode('utf8')
response = json.loads(response)
print(response)

#@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'home.html'

class group(TemplateView):
    template_name = 'grupo/grupo.html'

def create_group(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'grupo/criar_grupo.html')
    if request.method == 'POST':
        tudo = request.POST.copy()
        novo_grupo = Groups.objects.create(GpName=tudo["GpName"], GpStats=tudo["GpStats"])
        
        us_grup = UserGroups.objects.create(GpUse= user, Groups= novo_grupo)

        emails = str(tudo['GpUse'])
        emails = emails.replace("  ","")
        emails = emails.replace(" ","")
        emails = emails.split(',')
        users_nao_cadastrados = []

        for n in range(0,len(emails)):
            try:
                conv = User.objects.filter(email=emails[n])
                us_grup = UserGroups.objects.create(GpUse= conv, Groups= novo_grupo)
            except:
                users_nao_cadastrados.append(emails[n])
                print("usuario", emails[n], " não encontrado, convite enviado para e-mail informado.")
                
        if len(users_nao_cadastrados) >= 1 :
            return render(request, 'grupo/aviso_criar_grupo.html',{"aviso_email" : users_nao_cadastrados})

        return render(request, 'grupo/criar_grupo.html')

def list_group(request):
    user = request.user
    try:
        gpuser = UserGroups.objects.filter(GpUse=user)
    except:
        return render(request, 'grupo/grupo.html')


    print(gpuser)
    return render(request, 'grupo/grupo.html',{"grupos" : gpuser})

def edit_group(request):
    user = request.user
    #edit = Groups.objects.filter(GpUse=user).update(field1='some value')
    return 0

def create_financas(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'grupo/criar_grupo.html')
    if request.method == 'POST':
        tudo = request.POST.copy()
        #novo_grupo = Groups.objects.create(GpName=tudo["GpName"], GpStats=tudo["GpStats"])
    return 0

def edit_financas(request):
    user = request.user
    edit = Financas.objects.filter(GpUse=user).update(field1='some value')
    return 0

def create_caixas(request):
    user = request.user
    novo_grupo = Caixas.objects.create()
    return 0

def edit_caixa(request):
    user = request.user
    edit = Caixas.objects.filter(GpUse=user).update(field1='some value')
    return 0
