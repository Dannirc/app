# Generated by Django 3.0.4 on 2021-06-07 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0009_client_type_pay'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='tecnic',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.Tecnic', verbose_name='Nombre de Tecnico'),
        ),
    ]
