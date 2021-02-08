from django.contrib import admin
from .models import Disciplina,  HistoricoAluno, Turma,EstudosHistorico

class turma_admin(admin.ModelAdmin):
    filter_horizontal = ('disciplinas',)

# class historico_admin(admin.ModelAdmin):
#     filter_horizontal = ('turma',)

# Register your models here.
admin.site.register(Disciplina)
admin.site.register(Turma,turma_admin)
admin.site.register(HistoricoAluno)
admin.site.register(EstudosHistorico)



