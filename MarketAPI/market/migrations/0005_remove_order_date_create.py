# Generated by Django 4.0.3 on 2022-05-14 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_rename_data_orderstatus_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='date_create',
        ),
    ]