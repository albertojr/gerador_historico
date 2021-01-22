from django.db import models
from localflavor.br.br_states import STATE_CHOICES


class Aluno(models.Model):
    cod_aluno = models.AutoField(primary_key=True)
    nome_aluno = models.CharField(verbose_name='Nome', max_length=400,unique=True)
    dt_nascimento_aluno = models.DateField(verbose_name='Data de Nascimento')
    naturalidade_aluno = models.CharField(verbose_name='Naturalidade', 
                                          max_length=400)
    estado_aluno = models.CharField(verbose_name='Estado', max_length=40,
                                    choices=STATE_CHOICES)
    nacionalidade_aluno = models.CharField(max_length=50,
                                           verbose_name='Nacionalidade')
    filiacao_aluno = models.CharField(max_length=400,
                                      verbose_name='Filiação')
    
    def __str__(self):
        return "%s" % (self.nome_aluno)
    
    class Meta:
        managed = True
        db_table = 'aluno'
        