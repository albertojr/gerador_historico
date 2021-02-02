from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
from historico.models import HistoricoAluno,Turma,Disciplina
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from .forms import HistoricoForm
from django.template.loader import get_template, render_to_string
import tempfile
from aluno.models import Aluno



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
    #salvar/atualizar notas
    if request.method == 'POST':
        data = {}
        try:
            json_data = request.body
            json_data = json.loads(json_data)
                
        except e:
            data = {
                "texto_mensagem": 'Erro ao Salvar notas, Json com formato incorreto!!',
                "mensagem_botao": 'Clique em OK para continuar!',
                "icone_mensagem": 'info'}
            return JsonResponse(data)
        
        for item in json_data:
            i = 0
            for i in range(len(item['nomes_turma'])):
                verifica_nota = HistoricoAluno.objects.filter(aluno__cod_aluno=item['cod_aluno'],
                turma_historico__ano_turma=item['nomes_turma'][i],
                disciplina_historico__cod_disciplina=item['cod_disciplina'],
                turma_historico__status_turma=True).values('cod_historico')

                #se já tiver nota
                if verifica_nota:
                    atualizar_notas(verifica_nota,item,i)

                if not verifica_nota:
                    #se campo de nota não estiver vazio
                    if item['notas'][i] != "":
                        try:
                            turma = Turma.objects.get(ano_turma=item['nomes_turma'][i])
                            obj_historico = HistoricoAluno()
                            obj_historico.turma_historico = turma
                            obj_historico.aluno_id = item['cod_aluno']
                            obj_historico.disciplina_historico_id = item['cod_disciplina']
                            obj_historico.nota = float(item['notas'][i])

                            if item['eja1'] == True:
                                if item['nomes_turma'][i] == 1 or item['nomes_turma'][i] == 2 or item['nomes_turma'][i] == 3:
                                    obj_historico.tipo_eja ='eja1'
                                                
                            if item['eja2'] == True:
                                if item['nomes_turma'][i] == 4 or item['nomes_turma'][i] == 5:
                                    obj_historico.tipo_eja ='eja2'
                            
                            if item['eja3'] == True:
                                if item['nomes_turma'][i] == 6 or item['nomes_turma'][i] == 7:
                                    obj_historico.tipo_eja ='eja3'
                            
                            if item['eja4'] == True:
                                if item['nomes_turma'][i] == 8 or  item['nomes_turma'][i] ==  9:
                                    obj_historico.tipo_eja ='eja4'
                            
                            obj_historico.save()

                        except:
                            data = {
                                "texto_mensagem": 'Problemas ao Salvar Notas!!',
                                "mensagem_botao": 'Clique em OK para continuar!',
                                "icone_mensagem": 'error'}
                            return JsonResponse(data)
                        
                    elif item['notas'][i] == "":
                        try:
                            turma = Turma.objects.get(ano_turma=item['nomes_turma'][i])
                            obj_historico = HistoricoAluno()
                            obj_historico.turma_historico = turma
                            obj_historico.aluno_id = item['cod_aluno']
                            obj_historico.disciplina_historico_id = item['cod_disciplina']

                            if item['eja1'] == True:
                                if item['nomes_turma'][i] == 1 or item['nomes_turma'][i] == 2:
                                    obj_historico.tipo_eja = 'eja1'
                                    obj_historico.save()

                            if item['eja2'] == True:
                                if item['nomes_turma'][i] == 4:
                                    obj_historico.tipo_eja = 'eja2'
                                    obj_historico.save()                        
                            
                            if item['eja3'] == True:
                                if item['nomes_turma'][i] == 6:
                                    obj_historico.tipo_eja = 'eja3'
                                    obj_historico.save()  

                            if item['eja4'] == True:
                                if item['nomes_turma'][i] == 8:
                                    obj_historico.tipo_eja = 'eja4'
                                    obj_historico.save()
                        except:
                            data = {
                                "texto_mensagem": 'Problemas ao Salvar Notas!!',
                                "mensagem_botao": 'Clique em OK para continuar!',
                                "icone_mensagem": 'error'}
                            return JsonResponse(data)

        data = {
            "texto_mensagem": 'Notas salvas com sucesso!!',
            "mensagem_botao": 'Clique em OK para continuar!',
            "icone_mensagem": 'success'}  
        return JsonResponse(data)
    
    #puxar lista
    else:
        ls_turmas = list()
        ls_disciplinas = list()
        ls_ejas = list()
        tem_historico = False

        cod_aluno = request.GET.get('dropAluno')

        qsturmas = Turma.objects.filter(status_turma=True).values('cod_turma',
        'ano_turma','carga_hr','disciplinas')
        
        if HistoricoAluno.objects.filter(aluno__cod_aluno=cod_aluno):
            tem_historico = True
        
        for item in qsturmas:
            disciplina_na_lista = False

            qs_disciplina = Disciplina.objects.filter(cod_disciplina = item['disciplinas']).values(
                'cod_disciplina','nome_disciplina')

            if qs_disciplina:
                dict_disciplinas = {'cod_turma':item['cod_turma'],
                        'cod_disciplina':qs_disciplina[0]['cod_disciplina'],
                        'nome_disciplina':qs_disciplina[0]['nome_disciplina']}
            
                for lista in ls_disciplinas:
                    if qs_disciplina[0]['cod_disciplina'] == lista['cod_disciplina']:
                        disciplina_na_lista = True
                
                if not disciplina_na_lista:
                    ls_disciplinas.append(dict_disciplinas)

        for item in qsturmas.distinct('ano_turma'):
            dict_turmas = {}
            dict_turmas = {'cod_turma':item['cod_turma'],'ano_turma':item['ano_turma']}
            ls_turmas.append(dict_turmas)
        
        #add notas na disciplina
        for item in ls_disciplinas:
            ls_notas = list()
            for turmas in ls_turmas:
                qs_historicos = HistoricoAluno.objects.filter(aluno__cod_aluno =cod_aluno,
                disciplina_historico__cod_disciplina=item['cod_disciplina'],
                turma_historico__cod_turma=turmas['cod_turma']).values('nota','tipo_eja')

                if qs_historicos:
                    ls_notas.append(qs_historicos[0]['nota'])

                    if qs_historicos[0]['tipo_eja'] != None and qs_historicos[0]['tipo_eja'] not in ls_ejas:
                        ls_ejas.append(qs_historicos[0]['tipo_eja'])
                else:
                    ls_notas.append(None)
                
            item.update({'notas':ls_notas})

        data = {'turmas': ls_turmas,'disciplinas':ls_disciplinas,'ejas':ls_ejas,'historico':tem_historico}
        return JsonResponse(data)

def atualizar_notas(qsHistoricoNota,item,i):
    obj_historico = HistoricoAluno.objects.get(
        cod_historico=qsHistoricoNota[0]['cod_historico'])

    if item['notas'][i] != "":
        try:
            obj_historico.nota = float(item['notas'][i])

            if item['eja1'] == True:
                if item['nomes_turma'][i] == 1 or item['nomes_turma'][i] == 2 or item['nomes_turma'][i] == 3:
                    if item['nomes_turma'][i] == 1 or item['nomes_turma'][i] == 2:
                        obj_historico.nota = None
                    obj_historico.tipo_eja ='eja1'                 
                                
            if item['eja2'] == True:
                if item['nomes_turma'][i] == 4 or item['nomes_turma'][i] == 5:
                    if item['nomes_turma'][i] == 4:
                        obj_historico.nota = None
                    obj_historico.tipo_eja ='eja2'
            
            if item['eja3'] == True:
                if item['nomes_turma'][i] == 6 or item['nomes_turma'][i] == 7:
                    if item['nomes_turma'][i] == 6:
                        obj_historico.nota = None
                    obj_historico.tipo_eja ='eja3'
            
            if item['eja4'] == True:
                if item['nomes_turma'][i] == 8 or item['nomes_turma'][i] ==  9:
                    if item['nomes_turma'][i] == 8:
                        obj_historico.nota = None
                    obj_historico.tipo_eja ='eja4'
            
            obj_historico.save(update_fields=['nota','tipo_eja'])

        except:
            data = {
                "texto_mensagem": 'Problemas ao Salvar Notas!!',
                "mensagem_botao": 'Clique em OK para continuar!',
                "icone_mensagem": 'error'}
            return JsonResponse(data)
    
    #deletar notas
    else:
        deletar_notas(obj_historico,item)

def deletar_notas(obj_historico,item):
    '''Se a nota do front vier vazia e for diferente da nota já cadastrada, é pra deletar'''
    if obj_historico.nota != None:
        try:
            obj_historico.delete()
        except:
            data = {
                "texto_mensagem": 'Problemas ao Deletar Notas!!',
                "mensagem_botao": 'Clique em OK para continuar!',
                "icone_mensagem": 'error'}
            return JsonResponse(data)

    elif obj_historico.nota == None:
        if item['eja1'] == False or item['eja2'] == False or item['eja3'] == False or item['eja4'] == False:
            try:
                obj_historico.delete()
            except:
                data = {
                    "texto_mensagem": 'Problemas ao Deletar Notas!!',
                    "mensagem_botao": 'Clique em OK para continuar!',
                    "icone_mensagem": 'error'}
                return JsonResponse(data)

def relatorio_pdf(request,cod_aluno):
    

    qs_aluno = Aluno.objects.filter(cod_aluno=cod_aluno).values()
    
    if qs_aluno:
        ls_turmas = list()
        ls_disciplinas = list()
        ls_ejas = list()
        tem_historico = False
        dados_aluno = {}

        historicos = HistoricoAluno.objects.filter(aluno__cod_aluno=cod_aluno)

        qsturmas = Turma.objects.filter(status_turma=True).values('cod_turma',
        'ano_turma','carga_hr','disciplinas')

        for aluno in qs_aluno:
            dados_aluno = {'nome':aluno['nome_aluno'],
            'dt_nasc':aluno['dt_nascimento_aluno'].strftime("%d/%m/%Y"),
            'naturalidade':aluno['naturalidade_aluno'],
            'estado':aluno['estado_aluno'],'nacionalidade':aluno['nacionalidade_aluno'],
            'filiacao':aluno['filiacao_aluno']}
                
        if HistoricoAluno.objects.filter(aluno__cod_aluno=cod_aluno):
            tem_historico = True
        
        for item in qsturmas:
            disciplina_na_lista = False

            qs_disciplina = Disciplina.objects.filter(cod_disciplina = item['disciplinas']).values(
                'cod_disciplina','nome_disciplina','tipo_disciplina')

            if qs_disciplina:
                dict_disciplinas = {'cod_turma':item['cod_turma'],
                        'cod_disciplina':qs_disciplina[0]['cod_disciplina'],
                        'nome_disciplina':qs_disciplina[0]['nome_disciplina'],
                        'tp_disciplina':qs_disciplina[0]['tipo_disciplina']}
            
                for lista in ls_disciplinas:
                    if qs_disciplina[0]['cod_disciplina'] == lista['cod_disciplina']:
                        disciplina_na_lista = True
                
                if not disciplina_na_lista:
                    ls_disciplinas.append(dict_disciplinas)

        for item in qsturmas.distinct('ano_turma'):
            dict_turmas = {'cod_turma':item['cod_turma'],'ano_turma':item['ano_turma']}
            ls_turmas.append(dict_turmas)
        
        #add notas na disciplina
        for item in ls_disciplinas:
            ls_notas = list()
            for turmas in ls_turmas:
                qs_historicos = HistoricoAluno.objects.filter(aluno__cod_aluno =cod_aluno,
                disciplina_historico__cod_disciplina=item['cod_disciplina'],
                turma_historico__cod_turma=turmas['cod_turma']).values('nota','tipo_eja')

                if qs_historicos:
                    ls_notas.append(qs_historicos[0]['nota'])

                    if qs_historicos[0]['tipo_eja'] != None and qs_historicos[0]['tipo_eja'] not in ls_ejas:
                        ls_ejas.append(qs_historicos[0]['tipo_eja'])
                else:
                    ls_notas.append(None)
                
            item.update({'notas':ls_notas})

        return render(request, 'relatorios/historico_pdf.html',
            {'dados_aluno':dados_aluno,
            'turmas': ls_turmas,
            'disciplinas':ls_disciplinas,
            'ejas':ls_ejas,'historico':tem_historico,
            'qnt_disciplinas':len(ls_disciplinas)+1})
        
    else:
        return HttpResponse("nenhum aluno encontrato!")
        

class RenderPdf:
    '''classe padrão que converte o HTML para pdf'''
    @staticmethod
    def render(path: str, params: dict, filename: str, request):

        html_string = render_to_string(
           path, params)
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'attachment;filename=%s.pdf' % filename
        response['Content-Transfer-Encoding'] = 'binary'

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())

        return response