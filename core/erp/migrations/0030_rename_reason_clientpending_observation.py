# Generated by Django 3.2.7 on 2022-07-25 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0029_auto_20220703_2346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientpending',
            old_name='reason',
            new_name='observation',
        ),
    ]
