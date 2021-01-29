from django.db import models
from aluno.models import Aluno

tp_disciplina = (
    ('fundamental','Ensino Fundamental'),
    ('diversificada','Lingua Estrangeira')
)

anos_choice = (
    ('1', '1º Ano'),
    ('2', '2º Ano'),
    ('3', '3º Ano'),
    ('4', '4º Ano'),
    ('5', '5º Ano'),
    ('6', '6º Ano'),
    ('7', '7º Ano'),
    ('8', '8º Ano'),
    ('9', '9º Ano'),
)
ejas = (
    ('eja1', 'EJA1'),
    ('eja2', 'EJA2'),
    ('eja3', 'EJA3'),
    ('eja4', 'EJA4'),
)


class Disciplina(models.Model):
    cod_disciplina = models.AutoField(primary_key=True)
    nome_disciplina = models.CharField(verbose_name='Nome', max_length=300, unique=True)
    tipo_disciplina = models.CharField(verbose_name='Tipo de Disciplina',
                                       max_length=30, choices=tp_disciplina)

    def __str__(self):
        return '{} - {}'.format(self.cod_disciplina, self.nome_disciplina)

    class Meta:
        managed = True
        db_table = 'disciplina'


class Turma(models.Model):
    cod_turma = models.AutoField(primary_key=True)
    ano_turma = models.CharField(verbose_name="Ano", max_length=6, choices=anos_choice)
    disciplinas = models.ManyToManyField(Disciplina,related_name='turma_disciplinas')
    carga_hr = models.IntegerField(verbose_name="Oferta Anual")
    status_turma = models.BooleanField(default=True,verbose_name="Status da turma")

    def __str__(self):
        return '{}º Ano | Disciplinas({})'.format(self.ano_turma[:20], 
                ' - '.join(self.disciplinas.all().values_list('nome_disciplina',flat= True)))

    class Meta:
        managed = True
        db_table = 'turma'

class HistoricoAluno(models.Model):
    cod_historico = models.AutoField(primary_key=True)
    turma_historico = models.ForeignKey(Turma,verbose_name='Turmas',on_delete=models.CASCADE)
    disciplina_historico = models.ForeignKey(Disciplina,on_delete = models.CASCADE,blank=True, null=True)
    nota = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='Nota',blank=True, null=True)
    tipo_eja = models.CharField(verbose_name='EJA', choices=ejas,max_length=6,blank=True, null=True)
    aluno = models.ForeignKey('aluno.Aluno',related_name='alunos' ,on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'historico'
    
    def __str__(self):
        return '{}º Ano | Aluno:{} | EJA:{} | Nota:{}'.format(self.turma_historico.ano_turma,
        self.aluno.nome_aluno,self.tipo_eja,self.nota)