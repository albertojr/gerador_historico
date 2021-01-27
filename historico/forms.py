from django import forms
from django_select2 import forms as s2forms
from aluno.models import Aluno

class HistoricoAutoComplete(s2forms.Select2Widget):
    search_fields = [
        "nome_aluno__icontains",
    ]

    # def label_from_instance(PlanoAulaTurma):
    #     return str(obj.title).upper()

class HistoricoForm(forms.Form):
    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        widget=HistoricoAutoComplete(
            attrs={
                'data-class': 'form-control select2bs4',
                'data-id': 'drop-alunos',
                'data-width': '100%',
                'data-placeholder': 'Selecione um aluno',
                'data-dropdown-css-class': 'select2-gray',
            }
        )
    )

    class Meta:
        fields = ('aluno',)