# Generated by Django 3.1.5 on 2021-02-25 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aluno', '0003_auto_20210212_1226'),
        ('historico', '0020_auto_20210225_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ofertaanual',
            name='historico_oferta',
        ),
        migrations.AddField(
            model_name='ofertaanual',
            name='aluno',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='oferta_alunal_alunos', to='aluno.aluno'),
            preserve_default=False,
        ),
    ]