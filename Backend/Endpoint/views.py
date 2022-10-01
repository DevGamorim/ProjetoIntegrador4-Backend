from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
# Create your views here.

from Data.models import Users, Financas, Groups, Caixas

#@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'home.html'

def create_group(request):
    user = request.user
    novo_grupo = Groups.objects.create()
    return 0

def edit_group(request):
    user = request.user
    edit = Groups.objects.filter(GpUse=user).update(field1='some value')
    return 0

def create_financas(request):
    user = request.user
    novo_grupo = Financas.objects.create()
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