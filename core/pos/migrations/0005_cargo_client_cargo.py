# Generated by Django 4.0.2 on 2022-10-25 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0004_alter_client_servicio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Cargo',
                'verbose_name_plural': 'Cargos',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='client',
            name='cargo',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.PROTECT, to='pos.cargo', verbose_name='Cargo'),
            preserve_default=False,
        ),
    ]
