# Generated by Django 4.0.2 on 2022-10-25 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0006_remove_client_dni'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='into',
            name='iva',
        ),
        migrations.RemoveField(
            model_name='into',
            name='total',
        ),
        migrations.RemoveField(
            model_name='into',
            name='total_iva',
        ),
    ]
