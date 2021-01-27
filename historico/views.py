from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
from historico.models import HistoricoAluno,Turma,Disciplina
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from .forms import HistoricoForm


# Create your views here.
@login_required
# @group_required('admin', 'monitor')
def home_geral(request):
    return render(request,'index.html')

@login_required
def historicos_json(request):
    alunos_historico = HistoricoAluno.objects.all().distinct('aluno__cod_aluno').values('aluno__cod_aluno',
    'aluno__nome_aluno','aluno__dt_nascimento_aluno','aluno__filiacao_aluno')
    
    for historico in alunos_historico:
        historico['aluno__dt_nascimento_aluno'] =  historico['aluno__dt_nascimento_aluno'].strftime("%d/%m/%Y")

    historicos_json = json.dumps({"data": list(alunos_historico)},
                      cls=DjangoJSONEncoder)

    return HttpResponse(historicos_json)

@login_required
def historico(request):
    context = {}
    context['form'] = HistoricoForm()
        
    return render(request,'historico.html',context)

def tabela_notas_historico(request):
    cod_aluno = request.GET.get('dropAluno')
    historicos = HistoricoAluno.objects.filter(aluno__cod_aluno=cod_aluno)
    turmas = Turma.objects.all().values('cod_turma','ano_turma','carga_hr','disciplinas')
    
    print(turmas)
    # dict tabela_notas = {''}
    # print(turmas)
    for item in turmas:
        disciplina_turma = Disciplina.objects.filter(cod_disciplina = item['disciplinas']).values('cod_disciplina','nome_disciplina')
        
        print(disciplina_turma)
        # if hs_port_turma:
    #         print(hs_port_turma)
    data = {'turmas': list(turmas)}
    return JsonResponse(data)

