from django.contrib import admin

# Register your models here.
from .models import Users, Financas, Groups, Caixas

admin.site.register(Users)
admin.site.register(Financas)
admin.site.register(Groups)
admin.site.register(Caixas)