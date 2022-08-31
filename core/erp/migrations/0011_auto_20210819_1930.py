# Generated by Django 3.2 on 2021-08-19 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0010_client_tecnic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='cuit',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Cuit'),
        ),
        migrations.AlterField(
            model_name='client',
            name='position',
            field=models.IntegerField(blank=True, default=99, null=True, verbose_name='Posicion'),
        ),
    ]
