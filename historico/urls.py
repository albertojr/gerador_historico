
from historico import views
from django.urls import path

urlpatterns = [
    path('lista/alunos/json',views.historicos_json,name='historicos_json'),
    path('',views.historico,name='historico'),
    path('tabela/notas',views.tabela_notas_historico,name='tabela_notas'),
    path('relatorio/pdf/<int:cod_aluno>',views.relatorio_pdf,name='historico_relatorio_pdf')
]