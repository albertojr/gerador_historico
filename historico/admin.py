from django.contrib import admin
from .models import Disciplina,  HistoricoAluno, Turma,EstudosHistorico



# class historico_admin(admin.ModelAdmin):
#     filter_horizontal = ('turma',)

# Register your models here.
admin.site.register(Disciplina)
admin.site.register(Turma)
admin.site.register(HistoricoAluno)
admin.site.register(EstudosHistorico)



