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


#url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json&dataInicial=18/10/2022&dataFinal=18/10/2022"
#response = requests.request("GET", url)
#response = response.text.encode('utf8')
#response = json.loads(response)
#print(response)

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
                conv = User.objects.get(email=emails[n])
                us_grup = UserGroups.objects.create(GpUse= conv, Groups= novo_grupo)
            except:
                users_nao_cadastrados.append(emails[n])
                print("usuario", emails[n], " não encontrado, convite enviado para e-mail informado.")
                
        if len(users_nao_cadastrados) >= 1 :
            return render(request, 'grupo/aviso_criar_grupo.html',{"aviso_email" : users_nao_cadastrados})

        caixa = Caixas.objects.create(CaixaGrupo = novo_grupo, CaixaTotal = 0.0, CaixaStats =tudo["GpStats"])

        return render(request, 'grupo/criar_grupo.html')

def list_group(request):
    user = request.user
    try:
        gpuser = UserGroups.objects.filter(GpUse=user)
    except:
        return render(request, 'grupo/grupo.html')


    print(gpuser)
    return render(request, 'grupo/grupo.html',{"grupos" : gpuser})

def edit_group(request, id):
    user = request.user
    users = UserGroups.objects.filter(Groups=id)

    try:
        edit = Groups.objects.get(pk=id)
    except:
        try:
            gpuser = UserGroups.objects.filter(GpUse=user)
        except:
            return render(request, 'grupo/grupo.html')
        return render(request, 'grupo/grupo.html',{"grupos" : gpuser})


    if request.method == 'GET':

        all_users = ""
        for n in range(0,len(users)):
            print(users[n].GpUse.email)
            all_users = all_users + str(users[n].GpUse.email)+ ", "

        return render(request, 'grupo/editargrupo.html',{"grupo" : edit,"all_users":all_users})

    if request.method == 'POST':
        try:
            gpuser = UserGroups.objects.filter(GpUse=user)
        except:
            return render(request, 'grupo/grupo.html')

        tudo = request.POST.copy()

        emails = str(tudo['GpUse'])
        emails = emails.replace("  ","")
        emails = emails.replace(" ","")
        emails = emails.split(',')

        return render(request, 'grupo/grupo.html',{"grupos" : gpuser})

def home_caixas(request):
    user = request.user
    
    users = UserGroups.objects.filter(GpUse=user)

    caixas = []
    for n in range(0,len(users)):
        caixa = Caixas.objects.get(CaixaGrupo=users[n].Groups)
        caixas.append(caixa)
        print(caixas)
    return render(request, 'caixa/home_caixas.html',{"caixas" : caixas})
    
def edit_create_financas(request, id):
    user = request.user
    if request.method == 'GET':
        return render(request, 'grupo/criar_grupo.html')
    if request.method == 'POST':
        tudo = request.POST.copy()
        #novo_grupo = Groups.objects.create(GpName=tudo["GpName"], GpStats=tudo["GpStats"])
    return 0