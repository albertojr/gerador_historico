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
    ls_turmas = list()
    ls_disciplinas = list()

    cod_aluno = request.GET.get('dropAluno')
    qsturmas = Turma.objects.filter(status_turma=True).values('cod_turma','ano_turma','carga_hr','disciplinas')
    
    for item in qsturmas:
        qs_disciplina = Disciplina.objects.filter(cod_disciplina = item['disciplinas']).values(
            'cod_disciplina','nome_disciplina')
        lista_disciplina = False
        if qs_disciplina:
            dict_disciplinas = {'cod_turma':item['cod_turma'],
                    'cod_disciplina':qs_disciplina[0]['cod_disciplina'],
                    'nome_disciplina':qs_disciplina[0]['nome_disciplina']}
          
            for lista in ls_disciplinas:
                if qs_disciplina[0]['cod_disciplina'] == lista['cod_disciplina']:
                    lista_disciplina=True

            if not lista_disciplina:
                ls_disciplinas.append(dict_disciplinas)

    for item in qsturmas.distinct('ano_turma'):
        dict_turmas = {}
        dict_turmas = {'cod_turma':item['cod_turma'],'ano_turma':item['ano_turma']}
        ls_turmas.append(dict_turmas)
    print(ls_disciplinas)
    data = {'turmas': ls_turmas}
    return JsonResponse(data)

