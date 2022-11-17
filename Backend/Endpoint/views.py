from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
# Create your views here.

from Data.models import Financas, Groups, Caixas, Comentario, Selic, UserGroups, Caixas
from users.models import User

# libs import
import requests
from datetime import datetime
import json

#Libs para ia

#Importando bibliotenas
import string
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
import pickle
from wordcloud import WordCloud

# Pré-processamento e avaliação
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.regularizers import l1, l2

# Modelos
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB


url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json&dataInicial=18/10/2022&dataFinal=18/10/2022"
response = requests.request("GET", url)
response = response.text.encode('utf8')
response = json.loads(response)
print(response)

selicc = Selic.objects.get(pk=1)
selicc.Slvalue = float(response[0]['valor'])
selicc.save()


#@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'home.html'

class group(TemplateView):
    template_name = 'grupo/grupo.html'

@login_required
def home(request):
    user = request.user

    grupos = UserGroups.objects.filter(GpUse= user)
    grup = []
    for n in range(0,len(grupos)):
        if grupos[n].Groups in grup:
            continue
        else:
           grup.append(grupos[n].Groups)
    
    caixas = []
    for n in range(0,len(grup)):
        caixa = Caixas.objects.get(CaixaGrupo=grup[n])
        caixas.append(caixa)
    
    financas = []
    for n in range(0,len(caixas)):
        financa = Financas.objects.filter(CaixaFinanca=caixas[n])
        financas.append(financa)


    return render(request, 'home.html', {"caixas": caixas, "financas":financas})

@login_required
def create_group(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'grupo/criar_grupo.html')
    if request.method == 'POST':
        tudo = request.POST.copy()
        novo_grupo = Groups.objects.create(GpName=tudo["GpName"], GpStats=tudo["GpStats"])
        
        us_grup = UserGroups.objects.create(GpUse= user, Groups= novo_grupo)

        caixa = Caixas.objects.create(CaixaGrupo = novo_grupo, CaixaTotal = 0.0, CaixaStats =tudo["GpStats"])
        
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

        

        return render(request, 'grupo/criar_grupo.html')

@login_required
def list_group(request):
    user = request.user
    try:
        gpuser = UserGroups.objects.filter(GpUse=user)
    except:
        return render(request, 'grupo/grupo.html')


    print(gpuser)
    return render(request, 'grupo/grupo.html',{"grupos" : gpuser})

@login_required
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

@login_required
def home_caixas(request):
    user = request.user
    
    users = UserGroups.objects.filter(GpUse=user)

    caixas = []
    for n in range(0,len(users)):
        caixa = Caixas.objects.get(CaixaGrupo=users[n].Groups)
        caixas.append(caixa)
    return render(request, 'caixa/home_caixas.html',{"caixas" : caixas})
    
@login_required
def create_financas(request, id):
    user = request.user

    try:
        caixa = Caixas.objects.get(pk=id)
    except:
        return render(request, 'caixa/ver_caixa.html',{"id":id})

    try:
        financas = Financas.objects.filter(CaixaFinanca=caixa, FinancaStats=True)
    except:
        financas = ''
    

    if request.method == 'GET':

        return render(request, 'caixa/ver_caixa.html',{"financas" : financas,"id":id, "total": caixa.CaixaTotal})
    if request.method == 'POST':
        tudo = request.POST.copy()
        if tudo['tipo'] == 'novo':
            try:
                valor = str(tudo['FinancaValue'])
                valor = valor.replace(",",".")
                valor = float(valor)
                valor = round(valor, 2)
            except:
                return render(request, 'caixa/ver_caixa.html',{"financas" : financas,"id":id, "total": caixa.CaixaTotal})

            if tudo['FinancaType'] == "True":
                new_fianca = Financas.objects.create(FinancaUser = user, CaixaFinanca = caixa, FinancaType = True, FinancaValue = valor, FinancaName = tudo['FinancaName'], FinancaStats = True)
            else:
                new_fianca = Financas.objects.create(FinancaUser = user, CaixaFinanca = caixa, FinancaType = False, FinancaValue = valor, FinancaName = tudo['FinancaName'], FinancaStats = True)

            financas = Financas.objects.filter(CaixaFinanca=caixa, FinancaStats=True)

            total = 0
            total_positivo = 0
            total_negativo = 0
            for n in range(0,len(financas)):
                if financas[n].FinancaType == True:
                    total = total + financas[n].FinancaValue
                    total_positivo = total_positivo + financas[n].FinancaValue
                else:
                    total_negativo = total_negativo + financas[n].FinancaValue
                    total = total - financas[n].FinancaValue

            for n in range(0,len(financas)):
                if financas[n].FinancaType == True:
                    procentagem = financas[n].FinancaValue / total_positivo
                    procentagem = procentagem * 100
                    financas[n].Financaporcentagem = round(procentagem, 2)
                    financas[n].save()
                else:
                    procentagem = financas[n].FinancaValue / total_negativo
                    procentagem = procentagem * 100
                    financas[n].Financaporcentagem = round(procentagem, 2)
                    financas[n].save()

            caixa.CaixaTotal = round(total, 2)
            caixa.save()

            return render(request, 'caixa/ver_caixa.html',{"financas" : financas,"id":id, "total": caixa.CaixaTotal})
        else:
            
            if tudo['FinancaStats'] == 'False':
                id_ = int(tudo['tipo'])
                financas = Financas.objects.get(pk= id_)
                financas.FinancaStats = False
                financas.save()

                financas = Financas.objects.filter(CaixaFinanca=caixa, FinancaStats=True)

                total_positivo = 0
                total_negativo = 0
                for n in range(0,len(financas)):
                    if financas[n].FinancaType == True:
                        total = total + financas[n].FinancaValue
                        total_positivo = total_positivo + financas[n].FinancaValue
                    else:
                        total_negativo = total_negativo + financas[n].FinancaValue
                        total = total - financas[n].FinancaValue

                for n in range(0,len(financas)):
                    if financas[n].FinancaType == True:
                        procentagem = financas[n].FinancaValue / total_positivo
                        procentagem = procentagem * 100
                        financas[n].Financaporcentagem = round(procentagem, 2)
                        financas[n].save()
                    else:
                        procentagem = financas[n].FinancaValue / total_negativo
                        procentagem = procentagem * 100
                        financas[n].Financaporcentagem = round(procentagem, 2)
                        financas[n].save()

                caixa.CaixaTotal = round(total, 2)
                caixa.save()

                return render(request, 'caixa/ver_caixa.html',{"financas" : financas,"id":id, "total": caixa.CaixaTotal})
            else:
                id_ = int(tudo['tipo'])
                financas = Financas.objects.get(pk= id_)
                if tudo['FinancaName'] != '':
                    financas.FinancaName = tudo['FinancaName']
                if tudo['FinancaValue'] != '':
                    valor = str(tudo['FinancaValue'])
                    valor = valor.replace(",",".")
                    valor = float(valor)
                    valor = round(valor, 2)
                    financas.FinancaValue = valor
                if tudo['FinancaType'] != 'True':
                    financas.FinancaType = False
                financas.save()

                financas = Financas.objects.filter(CaixaFinanca=caixa, FinancaStats=True)

                total = 0
                total_positivo = 0
                total_negativo = 0
                for n in range(0,len(financas)):
                    if financas[n].FinancaType == True:
                        total = total + financas[n].FinancaValue
                        total_positivo = total_positivo + financas[n].FinancaValue
                    else:
                        total_negativo = total_negativo + financas[n].FinancaValue
                        total = total - financas[n].FinancaValue

                for n in range(0,len(financas)):
                    if financas[n].FinancaType == True:
                        procentagem = financas[n].FinancaValue / total_positivo
                        procentagem = procentagem * 100
                        financas[n].Financaporcentagem = round(procentagem, 2)
                        financas[n].save()
                    else:
                        procentagem = financas[n].FinancaValue / total_negativo
                        procentagem = procentagem * 100
                        financas[n].Financaporcentagem = round(procentagem, 2)
                        financas[n].save()
                caixa.CaixaTotal = total
                caixa.save()

                return render(request, 'caixa/ver_caixa.html',{"financas" : financas,"id":id, "total": caixa.CaixaTotal})

    return render(request, 'caixa/ver_caixa.html',{"financas" : financas,"id":id, "total": caixa.CaixaTotal})

def calc_juros_compostos(principal, periodo, juros): 
    """ CALCULADORA DE JUROS COMPOSTOS """
    montante = principal * ((1 + juros/100)**periodo)
    juros = montante-principal
    
    resultado = [round(juros, 2),round(montante, 2)]
    return resultado

@login_required
def calcular_objetivo(request):
    if request.method == 'GET':

        return render(request, 'caixa/calculo.html')
    if request.method == 'POST':
        tudo = request.POST.copy()            
        principal = float(tudo['principal'])
        periodo = int(tudo['periodo'])
        juros = float(tudo['juros'])

        resultado = calc_juros_compostos(principal, periodo, juros)

        return render(request, 'caixa/calculo.html',{"juros" : (resultado[0]),"montante":resultado[1], "total": principal,"periodo":periodo,"jurosmes": juros,})
    

# Regressão Logística
def ml_predict(text):
    clean_text = cleaning(text)
    tfid_matrix = tfid.transform([clean_text])
    pred = log.predict(tfid_matrix)[0]
    
    return pred

# Rede Neural
def dl_predict(text):
    clean_text = cleaning(text)
    seq = tokenizer.texts_to_sequences([clean_text])
    padded = pad_sequences(seq)

    pred = model.predict(padded)
    # Recuperar o nome do rótulo
    result = lb.inverse_transform(pred)[0]
    
    return result

@login_required
def comentarios(request):
    user = request.user
    if request.method == 'GET':
        try:
            coments = Comentario.objects.filter(CmUser=user)
        except:
            coments = ''
        return render(request, 'comentarios.html')
    if request.method == 'POST':
        tudo = request.POST.copy()
        
        coments = Comentario.objects.create(CmUser=user, CmMessage=tudo['mensagem'],CmScore=float(tudo['score']))

        try:
            coments = Comentario.objects.filter(CmUser=user)
        except:
            coments = ''

        return render(request, 'comentarios.html',{"coments" : coments})
    