# Generated by Django 3.1.5 on 2021-02-17 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historico', '0015_remove_turma_disciplinas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicoaluno',
            name='nota',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True, verbose_name='Nota'),
        ),
    ]
