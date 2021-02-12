# Generated by Django 3.1.5 on 2021-02-12 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0002_auto_20210127_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aluno',
            name='filiacao_aluno',
        ),
        migrations.AddField(
            model_name='aluno',
            name='filiacao_aluno1',
            field=models.CharField(default=1, max_length=250, verbose_name='Filiação(Pai)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aluno',
            name='filiacao_aluno2',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Filiação(Mãe)'),
        ),
    ]
