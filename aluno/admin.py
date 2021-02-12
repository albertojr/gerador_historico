from django.contrib import admin
from .models import Aluno

# Register your models here.
class AlunoAdmin(admin.ModelAdmin):
    search_fields = ('nome_aluno',)

admin.site.register(Aluno,AlunoAdmin)
