# Generated by Django 3.1.5 on 2021-02-22 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historico', '0016_auto_20210217_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicoaluno',
            name='nota',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, verbose_name='Nota'),
        ),
    ]
