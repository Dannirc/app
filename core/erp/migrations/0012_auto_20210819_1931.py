# Generated by Django 3.2 on 2021-08-19 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0011_auto_20210819_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='cuit',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Cuit'),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Nombre o Razon Social'),
        ),
    ]