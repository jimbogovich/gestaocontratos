# Generated by Django 4.2.23 on 2025-07-08 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestaodecontratos', '0014_reminder_visualizado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmanagement_db',
            name='type_contract',
            field=models.CharField(choices=[('manutencao', 'Manutenção'), ('servicos', 'Serviços'), ('suprimentos', 'Suprimentos'), ('Internet', 'Internet'), ('telefonia', 'Telefonia')], max_length=100, null=True, verbose_name='Contract Type'),
        ),
    ]
