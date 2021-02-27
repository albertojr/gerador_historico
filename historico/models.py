from django.db import models
from aluno.models import Aluno
from localflavor.br.br_states import STATE_CHOICES


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
    historico_base = models.BooleanField(default=False)

    def __str__(self):
        return '{} - Base: {}'.format(self.nome_disciplina,self.historico_base)

    class Meta:
        managed = True
        db_table = 'disciplina'


class Turma(models.Model):
    cod_turma = models.AutoField(primary_key=True)
    ano_turma = models.CharField(verbose_name="Ano", max_length=6, choices=anos_choice)
    status_turma = models.BooleanField(default=True,verbose_name="Status da turma")

    class Meta:
        managed = True
        db_table = 'turma'
    
    def __str__(self):
        return '{} - {}º Ano'.format(self.cod_turma,self.ano_turma)

class HistoricoAluno(models.Model):
    cod_historico = models.AutoField(primary_key=True)
    turma_historico = models.ForeignKey(Turma,verbose_name='Turmas',on_delete=models.CASCADE)
    disciplina_historico = models.ForeignKey(Disciplina,on_delete = models.CASCADE,blank=True, null=True)
    nota = models.DecimalField(max_digits=3, decimal_places=1,verbose_name='Nota',blank=True, null=True)
    tipo_eja = models.CharField(verbose_name='EJA', choices=ejas,max_length=6,blank=True, null=True)
    aluno = models.ForeignKey('aluno.Aluno',related_name='alunos' ,on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'historico'
    
    def __str__(self):
        return '{} | cod.{} {}º Ano | Aluno:{} | EJA:{} | Nota:{}'.format(
            self.disciplina_historico.nome_disciplina,self.cod_historico,self.turma_historico.ano_turma,
        self.aluno.nome_aluno,self.tipo_eja,self.nota)

class EstudosHistorico(models.Model):
    cod_estudos_historico = models.AutoField(primary_key=True)
    historico_estudo = models.ForeignKey('HistoricoAluno',on_delete=models.CASCADE,null=True)
    ano_turma_estudo = models.ForeignKey('Turma',on_delete=models.CASCADE,null=True)
    ano_letivo_estudo = models.DateField(null=True)
    escola_ensino_estudo = models.CharField(max_length=200,null=True)
    municipio_estudo = models.CharField(max_length=200,null=True)
    estado_estudo = models.CharField(max_length=2,choices=STATE_CHOICES,null=True)
    resultado_estudo = models.CharField(max_length=15,null=True)

    class Meta:
        managed = True
        db_table = 'estudos_historico'

class OfertaAnual(models.Model):
    cod_oferta_anual = models.AutoField(primary_key=True)
    historico_aluno = models.ForeignKey('HistoricoAluno',verbose_name="Aluno",on_delete=models.CASCADE)
    turma_ch_anual = models.ForeignKey('Turma',verbose_name="Turma",on_delete=models.CASCADE)
    ch_hr_anual = models.IntegerField(verbose_name="Carga Horaria")

    class Meta:
        managed = True
        db_table = 'oferta_anual'

    def __str__ (self):
        return 'cod.{} | {} | {}º Ano | C.H {}'.format(self.cod_oferta_anual,
        self.historico_aluno.aluno.nome_aluno,
        self.historico_aluno.turma_historico.ano_turma,
        self.ch_hr_anual)




