
from historico import views
from django.urls import path

urlpatterns = [
    path('lista/alunos/json',views.historicos_json,name='historicos_json'),
    path('add/<int:cod_aluno>',views.add_form_line_historico,name='add_historicos'),
    path('update/<int:cod_aluno>',views.update_form_line_historico,name='update_historicos'),
    path('tabela/notas',views.tabela_notas_historico,name='tabela_notas'),
    path('tabela/estudos',views.salvar_estudos,name='tabela_estudos'),
    path('tabela/ofertaanual',views.oferta_anual,name='tabela_oferta_anual'),
    path('relatorio/pdf/<int:cod_aluno>',views.relatorio_pdf,name='historico_relatorio_pdf')
]