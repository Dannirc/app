# Generated by Django 3.0.4 on 2021-05-22 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0007_auto_20210516_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='pay',
            name='cheque',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True, verbose_name='Cheque'),
        ),
        migrations.AddField(
            model_name='pay',
            name='efectivo',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True, verbose_name='Efectivo'),
        ),
    ]
