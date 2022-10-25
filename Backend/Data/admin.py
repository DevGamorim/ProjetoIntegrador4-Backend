from django.contrib import admin

# Register your models here.
from .models import Financas, Groups, Caixas, Comentario, Selic


admin.site.register(Financas)
admin.site.register(Groups)
admin.site.register(Caixas)
admin.site.register(Comentario)
admin.site.register(Selic)