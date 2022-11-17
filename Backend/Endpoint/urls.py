from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'Endpoint'

urlpatterns =[
    path('', views.home, name='home' ),
    path('grupo/', views.group.as_view(), name='grupo' ),
    path('novogrupo/', views.create_group, name='novogrupo' ),
    path('editargrupo/<int:id>/', views.edit_group, name='editargrupo'),
    path('meusgrupos/', views.list_group, name='meusgrupos' ),
    path('minhascarteiras/', views.home_caixas, name='minhascarteiras' ),
    path('vercarteira/<int:id>/', views.create_financas, name='vercarteira' ),
    path('calcularobjetico/', views.calcular_objetivo, name='calcularobjetico'),
    path('comentarios/', views.comentarios, name='comentarios'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)