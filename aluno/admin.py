from django.contrib import admin
from .models import Aluno

# Register your models here.
class AlunoAdmin(admin.ModelAdmin):
 
    list_display = ('cod_aluno', 'nome_aluno','dt_nascimento_aluno', 'filiacao_aluno1','filiacao_aluno2')
    search_fields = ('nome_aluno',)

admin.site.register(Aluno,AlunoAdmin)
