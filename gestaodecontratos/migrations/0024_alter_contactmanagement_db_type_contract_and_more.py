# Generated by Django 4.2.23 on 2025-07-16 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestaodecontratos', '0023_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmanagement_db',
            name='type_contract',
            field=models.CharField(choices=[('manutencao', 'Manutenção'), ('servicos', 'Serviços'), ('suprimentos', 'Suprimentos'), ('internet', 'Internet'), ('telefonia', 'Telefonia')], max_length=100, null=True, verbose_name='Contract Type'),
        ),
        migrations.AlterField(
            model_name='documento',
            name='tipo',
            field=models.CharField(blank=True, choices=[('manutencao', 'Manutenção'), ('servicos', 'Serviços'), ('suprimentos', 'Suprimentos'), ('internet', 'Internet'), ('telefonia', 'Telefonia')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='reminder_type',
            field=models.CharField(blank=True, choices=[('manutencao', 'Manutenção'), ('servicos', 'Serviços'), ('suprimentos', 'Suprimentos'), ('internet', 'Internet'), ('telefonia', 'Telefonia')], max_length=100, null=True, verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='tipocontratos',
            name='tipos',
            field=models.CharField(choices=[('manutencao', 'Manutenção'), ('servicos', 'Serviços'), ('suprimentos', 'Suprimentos'), ('internet', 'Internet'), ('telefonia', 'Telefonia')], max_length=100),
        ),
    ]
