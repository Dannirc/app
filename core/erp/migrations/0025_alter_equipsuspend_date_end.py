# Generated by Django 3.2.7 on 2022-04-02 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0024_equipremove_equipsuspend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipsuspend',
            name='date_end',
            field=models.DateField(verbose_name='Fecha de Reactivación'),
        ),
    ]