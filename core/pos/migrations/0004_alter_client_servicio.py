# Generated by Django 4.0.2 on 2022-10-23 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0003_alter_sale_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.servicio', verbose_name='Servicio a que Pertenece'),
        ),
    ]
