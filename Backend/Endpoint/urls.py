

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'Endpoint'

urlpatterns =[
    path('', views.HomePageView.as_view(), name='home' ),
    path('grupo/', views.group.as_view(), name='grupo' ),
    path('novogrupo/', views.create_group, name='novogrupo' ),
    path('meusgrupos/', views.list_group, name='meusgrupos' ),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)