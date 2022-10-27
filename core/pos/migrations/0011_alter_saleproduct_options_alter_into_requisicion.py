# Generated by Django 4.0.2 on 2022-10-26 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0010_into_date_joined'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='saleproduct',
            options={'default_permissions': (), 'ordering': ['id'], 'verbose_name': 'Detalle de Solicitud', 'verbose_name_plural': 'Detalle de Solicitudes'},
        ),
        migrations.AlterField(
            model_name='into',
            name='requisicion',
            field=models.IntegerField(verbose_name='No_requisicion'),
        ),
    ]
