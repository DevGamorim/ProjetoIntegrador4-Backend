from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
# Create your views here.

#@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'home.html'