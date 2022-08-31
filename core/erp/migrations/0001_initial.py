# Generated by Django 3.1.5 on 2021-02-16 18:27

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Abono',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre del producto')),
                ('price', models.FloatField(default=0.0)),
            ],
            options={
                'verbose_name': 'Abono',
                'verbose_name_plural': 'Abonos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre o Razon Social')),
                ('cuit', models.CharField(max_length=10, unique=True, verbose_name='Cuit')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('address', models.CharField(blank=True, max_length=150, null=True, verbose_name='Dirección')),
                ('cant', models.IntegerField(default=0)),
                ('enable', models.BooleanField(default=True)),
                ('odorizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.abono')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cli', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.client')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.client')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.sale')),
            ],
            options={
                'verbose_name': 'Cobro',
                'verbose_name_plural': 'Cobros',
                'ordering': ['id'],
            },
        ),
    ]