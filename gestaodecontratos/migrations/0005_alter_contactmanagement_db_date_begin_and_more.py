# Generated by Django 4.2.23 on 2025-06-30 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestaodecontratos', '0004_alter_contactmanagement_db_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmanagement_db',
            name='date_begin',
            field=models.DateField(verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='contactmanagement_db',
            name='date_end',
            field=models.DateField(verbose_name='End Date'),
        ),
    ]
