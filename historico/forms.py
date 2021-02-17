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

class HistoricoForm(forms.Form):
    alunos = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        widget=AlunoAutoComplete(
            attrs={
                'data-class': 'form-control select2bs4',
                'data-id': 'drop-alunos',
                'data-width': '100%',
                'data-placeholder': 'Clique aqui',
                'data-dropdown-css-class': 'select2-gray',
            }
        )
    )

    class Meta:
        model = HistoricoAluno
        fields = ('aluno',)

class Form_tabela_historico(forms.ModelForm):
    disciplinas = forms.ModelChoiceField(
        queryset=Disciplina.objects.all().order_by('nome_disciplina'),
    )

    class Meta:
        model = HistoricoAluno
        fields = ('nota','disciplinas','aluno')

    