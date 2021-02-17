from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
from historico.models import HistoricoAluno,Turma,Disciplina,EstudosHistorico
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime,date
from .forms import HistoricoForm,Form_tabela_historico
from django.template.loader import get_template, render_to_string
import tempfile
from aluno.models import Aluno
from weasyprint import HTML, CSS
from django.forms.models import inlineformset_factory


# Create your views here.
@login_required
# @group_required('admin', 'monitor')
def home_geral(request):
    return render(request,'index.html')

@login_required
def historicos_json(request):
    alunos_historico = HistoricoAluno.objects.all().distinct('aluno__cod_aluno').values('aluno__cod_aluno',
    'aluno__nome_aluno','aluno__dt_nascimento_aluno','aluno__filiacao_aluno1','aluno__filiacao_aluno2')
    
    for historico in alunos_historico:
        historico['aluno__dt_nascimento_aluno'] =  historico['aluno__dt_nascimento_aluno'].strftime("%d/%m/%Y")

    historicos_json = json.dumps({"data": list(alunos_historico)},
                      cls=DjangoJSONEncoder)

    return HttpResponse(historicos_json)

@login_required
def historico(request):
    context = {}
    historico_form = HistoricoAluno()
    notas_order_formset = inlineformset_factory(Disciplina,HistoricoAluno, form=Form_tabela_historico, 
    extra=8, can_delete=True, min_num=1, validate_min=True)

    if request.method == 'POST':
        forms = Form_tabela_historico(request.POST, request.FILES, instance=historico_form, prefix='main')
        formset = item_order_formset(request.POST, request.FILES, instance=historico_form, prefix='notas')

        if forms.is_valid() and formset.is_valid():
            forms = forms.save(commit=False)
            forms.save()
            formset.save()
            return HttpResponseRedirect('/historicos/')

    else:
        forms = Form_tabela_historico(instance=historico_form, prefix='main')
        formset = notas_order_formset(instance=historico_form, prefix='notas')

    context = {
        'forms': forms,
        'formset': formset,
    }
    print(context['formset'][0])
    return render(request, 'historico.html', context)

@login_required
def add_historico(request):
    context = {}
    aluno_form = HistoricoForm()
    historico_form = HistoricoAluno()
    notas_order_formset = inlineformset_factory(Disciplina,HistoricoAluno, form=historico_form, extra=1, can_delete=False, min_num=1, validate_min=True)

    if request.method == 'POST':
        forms = Form_tabela_historico(request.POST, request.FILES, instance=historico_form, prefix='main')
        formset = item_order_formset(request.POST, request.FILES, instance=historico_form, prefix='notas')

        if forms.is_valid() and formset.is_valid():
            forms = forms.save(commit=False)
            forms.save()
            formset.save()
            return HttpResponseRedirect('/historicos/')

    else:
        forms = Form_tabela_historico(instance=order_forms, prefix='main')
        formset = notas_order_formset(instance=order_forms, prefix='notas')

    context = {
        'forms': forms,
        'formset': formset,
    }
    print(context['formset'][0])
    return render(request, 'historico.html', context)




@login_required
def tabela_notas_historico(request):
    #salvar/atualizar notas
    if request.method == 'POST':
        data = {}
        try:
            json_data = request.body
            json_data = json.loads(json_data)
                
        except:
            data = {"success": False, "error": "Erro ao Salvar notas, Json com formato incorreto!!"}        
            return JsonResponse(data,status=404)
        
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
                            data = {"success": False, "error": "Problemas ao Salvar Notas!!"}
                            return JsonResponse(data,status=404)
                        
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
                            data = {"success": False, "error": "Problemas ao Salvar Notas!!"}                            
                            return JsonResponse(data,status=404)
        
        data = {"success": "Notas salvas com sucesso!"}                            
        return JsonResponse(data)
    
    #puxar lista
    else:
        ls_turmas = list()
        ls_disciplinas = list()
        ls_ejas = list()
        ls_estudos_feitos = list()
        tem_historico = False

        cod_aluno = request.GET.get('dropAluno')

        qsturmas = Turma.objects.filter(status_turma=True).values('cod_turma',
        'ano_turma','carga_hr')
        
        if HistoricoAluno.objects.filter(aluno__cod_aluno=cod_aluno):
            tem_historico = True
        
        # for item in qsturmas.distinct("disciplinas__turma_disciplinas__disciplinas__cod_disciplina"):
        #     disciplina_na_lista = False
                       
        #     # if qs_disciplina:
        #     dict_disciplinas = {'cod_turma':item['cod_turma'],
        #             'cod_disciplina':item['disciplinas__turma_disciplinas__disciplinas__cod_disciplina'],
        #             'nome_disciplina':item['disciplinas__turma_disciplinas__disciplinas__nome_disciplina']}
        
        #     for ls_disciplina_pronta in ls_disciplinas:
        #         if item['disciplinas__turma_disciplinas__disciplinas__cod_disciplina'] == ls_disciplina_pronta['cod_disciplina']:
        #             disciplina_na_lista = True
            
        #     if not disciplina_na_lista:
        #         ls_disciplinas.append(dict_disciplinas)

        for item in qsturmas.distinct('ano_turma'):
            dict_turmas = {}
            dict_estudos = {'ano_turma':item['ano_turma'],'ano_letivo':'','escola':'',
            'municipio':'','uf':'','resultado':''}

            dict_turmas = {'cod_turma':item['cod_turma'],'ano_turma':item['ano_turma']}
            ls_turmas.append(dict_turmas)

            qs_estudos = EstudosHistorico.objects.filter(historico_estudo__aluno__cod_aluno=cod_aluno,
            ano_turma_estudo__ano_turma=item['ano_turma']).values('ano_turma_estudo__ano_turma','escola_ensino_estudo',
            'municipio_estudo','estado_estudo','resultado_estudo','ano_letivo_estudo')

            if qs_estudos:
                for estudos in qs_estudos:
                    if not estudos['ano_letivo_estudo']:
                        dict_estudos['ano_letivo'] = ""
                    else:
                        dict_estudos['ano_letivo'] = estudos['ano_letivo_estudo'].strftime("%Y")
                    dict_estudos['escola'] = estudos['escola_ensino_estudo']
                    dict_estudos['municipio'] = estudos['municipio_estudo']
                    dict_estudos['uf'] = estudos['estado_estudo']
                    dict_estudos['resultado'] = estudos['resultado_estudo']
            ls_estudos_feitos.append(dict_estudos)
        
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

        data = {'turmas': ls_turmas,'disciplinas':ls_disciplinas,
        'ejas':ls_ejas,'historico':tem_historico,
        'estudos_feitos':ls_estudos_feitos}
        return JsonResponse(data)

def atualizar_notas(qsHistoricoNota,item,i):
    obj_historico = HistoricoAluno.objects.get(
        cod_historico=qsHistoricoNota[0]['cod_historico'])

    if item['notas'][i] != "":
        try:
            obj_historico.nota = float(item['notas'][i])
            obj_historico.tipo_eja = None

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
            data = {"success": False, "error": "Problemas ao Atualizar Notas!!"}
            return JsonResponse(data,status=404)
    
    #deletar notas
    else:
        deletar_notas(obj_historico,item)

def deletar_notas(obj_historico,item):
    '''Se a nota do front vier vazia e for diferente da nota já cadastrada, é pra deletar'''
    if obj_historico.nota != None:
        try:
            obj_historico.delete()
        except:
            data = {"success": False, "error": "Problemas ao Deletar Notas!!"}
            return JsonResponse(data,status=404)

    elif obj_historico.nota == None:
        if item['eja1'] == False or item['eja2'] == False or item['eja3'] == False or item['eja4'] == False:
            try:
                obj_historico.delete()
            except:
                data = {"success": False, "error": "Problemas ao Deletar Notas!!"}
                return JsonResponse(data,status=404)

@login_required
def salvar_estudos(request):
    if request.method == 'POST':
        data = {}
        try:
            json_data = request.body
            json_data = json.loads(json_data)
                
        except:
            data = {"success": False, "error": "Erro ao Salvar notas, Json com formato incorreto!!"}        
            return JsonResponse(data,status=404)
        
        qs_historico = HistoricoAluno.objects.filter(aluno__cod_aluno=json_data[0]['cod_aluno']).first()
   
        if qs_historico:
            for json_estudos in json_data:
                json_cod_aluno = json_estudos['cod_aluno']
                json_ano_turma = json_estudos['turma'][0]
                ano_letivo = json_estudos['ano_letivo']
                if ano_letivo == '':
                    ano_letivo = None
                else:
                    ano_letivo = "01/01/"+ano_letivo
                    ano_letivo = datetime.strptime(ano_letivo, '%d/%m/%Y').date()

                qs_estudos_realizados = EstudosHistorico.objects.filter(historico_estudo__aluno__cod_aluno=json_cod_aluno,
                ano_turma_estudo__ano_turma=json_ano_turma).first()

                if not qs_estudos_realizados:
                    #salvar tanela de estudos
                    qs_estudos_realizados = EstudosHistorico()
                try:
                    qs_estudos_realizados.historico_estudo = qs_historico
                    qs_estudos_realizados.ano_turma_estudo = Turma.objects.get(ano_turma=json_ano_turma)
                    qs_estudos_realizados.ano_letivo_estudo = ano_letivo  
                    qs_estudos_realizados.escola_ensino_estudo = json_estudos['escola']
                    qs_estudos_realizados.municipio_estudo = json_estudos['cidade']
                    qs_estudos_realizados.estado_estudo = json_estudos['estado'].upper()
                    qs_estudos_realizados.resultado_estudo = json_estudos['resultado']
                    qs_estudos_realizados.save()
                
                except Exception as e:
                    print(e)
                    data = {"success": False, "error": "Problemas ao salvar/atulizar Estudos!!"}
                    return JsonResponse(data,status=404)              
        else:
            #não tem historico salvo ainda!
            data = {"error": "Nenhum histórico encontrado! por favor grave as notas antes de salvar os estudos!"}
            return JsonResponse(data,status=404)
    
    data = {"success": "Estudos salvos com sucesso!"}                            
    return JsonResponse(data)

def relatorio_pdf(request,cod_aluno):
    qs_aluno = Aluno.objects.filter(cod_aluno=cod_aluno).values()
    
    if qs_aluno:
        ls_turmas = list()
        ls_disciplinas = list()
        ls_estudos_feitos = list()
        tem_historico = False
        dados_aluno = {}
        ejas = {'eja1':False,'eja2':False,'Eja3':False,'Eja4':False}
       

        historicos = HistoricoAluno.objects.filter(aluno__cod_aluno=cod_aluno)

        qsturmas = Turma.objects.filter(status_turma=True).values('cod_turma',
        'ano_turma','carga_hr','disciplinas__turma_disciplinas__disciplinas__cod_disciplina',
        'disciplinas__turma_disciplinas__disciplinas__nome_disciplina',
        'disciplinas__turma_disciplinas__disciplinas__tipo_disciplina')

        for aluno in qs_aluno:
            dados_aluno = {'nome':aluno['nome_aluno'].upper(),
            'dt_nasc':aluno['dt_nascimento_aluno'].strftime("%d/%m/%Y"),
            'naturalidade':aluno['naturalidade_aluno'].upper(),
            'estado':aluno['estado_aluno'].upper(),
            'nacionalidade':aluno['nacionalidade_aluno'].upper(),
            'filiacao_1':aluno['filiacao_aluno1'].upper(),
            'filiacao_2':''}

            if aluno['filiacao_aluno2'] != None:
                dados_aluno['filiacao_2'] = aluno['filiacao_aluno2'].upper()
           
                        
        for item in qsturmas.distinct("disciplinas__turma_disciplinas__disciplinas__cod_disciplina"):
            disciplina_na_lista = False
                       
            # if qs_disciplina:
            dict_disciplinas = {'cod_turma':item['cod_turma'],
            'cod_disciplina':item['disciplinas__turma_disciplinas__disciplinas__cod_disciplina'],
            'nome_disciplina':item['disciplinas__turma_disciplinas__disciplinas__nome_disciplina'].upper(),
            'tp_disciplina':item['disciplinas__turma_disciplinas__disciplinas__tipo_disciplina']}
        
            for ls_disciplina_pronta in ls_disciplinas:
                if item['disciplinas__turma_disciplinas__disciplinas__cod_disciplina'] == ls_disciplina_pronta['cod_disciplina']:
                    disciplina_na_lista = True
            
            if not disciplina_na_lista:
                ls_disciplinas.append(dict_disciplinas)
            
        for item in qsturmas.distinct('ano_turma'):
            dict_turmas = {'cod_turma':item['cod_turma'],
            'ano_turma':item['ano_turma'],
            'ch':item['carga_hr']
            }
            ls_turmas.append(dict_turmas)

            qs_estudos = EstudosHistorico.objects.filter(historico_estudo__aluno__cod_aluno=cod_aluno,
            ano_turma_estudo__ano_turma=item['ano_turma']).order_by("ano_turma_estudo__ano_turma").values('ano_turma_estudo__ano_turma','escola_ensino_estudo',
            'municipio_estudo','estado_estudo','resultado_estudo','ano_letivo_estudo')

            if qs_estudos:
                dict_estudos = {'ano_turma':item['ano_turma'],'ano_letivo':'','escola':'',
                'municipio':'','uf':'','resultado':''}
                for estudos in qs_estudos:
                    if not estudos['ano_letivo_estudo']:
                        dict_estudos['ano_letivo'] = ""
                    else:
                        dict_estudos['ano_letivo'] = estudos['ano_letivo_estudo'].strftime("%Y")
                    
                    dict_estudos['escola'] = estudos['escola_ensino_estudo'].upper()
                    dict_estudos['municipio'] = estudos['municipio_estudo'].upper()
                    dict_estudos['uf'] = estudos['estado_estudo'].upper()
                    dict_estudos['resultado'] = estudos['resultado_estudo']
                ls_estudos_feitos.append(dict_estudos)
        
        #add notas na disciplina
        for item in ls_disciplinas:
            ls_notas = list()
            for turmas in ls_turmas:
                qs_historicos = HistoricoAluno.objects.filter(aluno__cod_aluno =cod_aluno,
                disciplina_historico__cod_disciplina=item['cod_disciplina'],
                turma_historico__cod_turma=turmas['cod_turma']).values('nota','tipo_eja')

                if qs_historicos:
                    ls_notas.append(qs_historicos[0]['nota'])

                    if qs_historicos[0]['tipo_eja'] != None:
                        if qs_historicos[0]['tipo_eja'] == 'eja1':
                            ejas['eja1'] = True

                        elif qs_historicos[0]['tipo_eja'] == 'eja2':
                            ejas['eja2'] = True

                        elif qs_historicos[0]['tipo_eja'] == 'eja3':
                            ejas['eja3'] = True
                        
                        elif qs_historicos[0]['tipo_eja'] == 'eja4':
                                ejas['eja4'] = True
                else:
                    ls_notas.append(None)
                
            item.update({'notas':ls_notas})

        params =  {'dados_aluno':dados_aluno,
            'turmas': ls_turmas,
            'estudos_feitos':ls_estudos_feitos,
            'disciplinas':ls_disciplinas,
            'tipo_eja':ejas,
            'historico':tem_historico,
            'qnt_disciplinas':len(ls_disciplinas)+3,
            'data':data_hoje()}

        return RenderPdf.render('relatorios/historico_pdf.html', 
        params, 
        'Histórico - '+dados_aluno['nome'], request)
        # return render(request, 'relatorios/historico_pdf.html',
        #     params)
        
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

def data_hoje():
    data_de_hoje = datetime.now()
    meses_ptbr = ["","janeiro", "fevereiro", "março", "abril", "maio", "junho",
                "julho", "agosto", "setembro", "outubro", "novembro",
                "dezembro"]
    mes_atual = int(data_de_hoje.strftime("%m"))
    data_historico = data_de_hoje.strftime(
        "%d de "+meses_ptbr[mes_atual]+" de %Y")
    return data_historico