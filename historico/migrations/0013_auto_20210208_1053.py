# Generated by Django 3.1.5 on 2021-02-08 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('historico', '0012_auto_20210208_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudoshistorico',
            name='historico_estudo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='historico.historicoaluno'),
        ),
    ]
