from django import forms
from django_select2 import forms as s2forms
from aluno.models import Aluno
from historico.models import HistoricoAluno,Disciplina

class AlunoAutoComplete(s2forms.Select2Widget):
    search_fields = [
        "nome_aluno__icontains",
    ]


class DisciplinaSelect2(s2forms.Select2Widget):
    search_fields = [
        "nome_disciplina__icontains",
    ]

class BuscaHistoricoForm(forms.Form):
    alunos = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        required=True,
    )

    class Meta:
        model = HistoricoAluno
        fields = ('aluno',)

class Form_tabela_historico(forms.ModelForm):
    disciplinas = forms.ModelChoiceField(
        queryset=Disciplina.objects.all().order_by('nome_disciplina'),
        required=True,
    )

    class Meta:
        model = HistoricoAluno
        fields = ('nota','disciplinas')
