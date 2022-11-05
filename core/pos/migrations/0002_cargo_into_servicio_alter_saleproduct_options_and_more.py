# Generated by Django 4.0.2 on 2022-11-05 17:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0001_initial'),
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
        migrations.CreateModel(
            name='Into',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('requisicion', models.IntegerField(null=True, verbose_name='No_requisicion')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
            options={
                'verbose_name': 'Entrada',
                'verbose_name_plural': 'Entradas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre del Servicio')),
                ('desc', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
                'ordering': ['id'],
            },
        ),
        migrations.AlterModelOptions(
            name='saleproduct',
            options={'default_permissions': (), 'ordering': ['id'], 'verbose_name': 'Detalle de Solicitud', 'verbose_name_plural': 'Detalle de Solicitudes'},
        ),
        migrations.RemoveField(
            model_name='client',
            name='dni',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='iva',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='total',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='total_iva',
        ),
        migrations.AddField(
            model_name='sale',
            name='requisicion',
            field=models.CharField(default=232, max_length=10, unique=True, verbose_name='No Requisicion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='mobile',
            field=models.CharField(max_length=8, verbose_name='Teléfono Institucional'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Centro de Salud'),
        ),
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=models.CharField(max_length=8, verbose_name='Teléfono Fax'),
        ),
        migrations.AlterField(
            model_name='company',
            name='ruc',
            field=models.CharField(max_length=13, verbose_name='NIT'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.category', verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_inventoried',
            field=models.BooleanField(default=True, verbose_name='¿Es invetario inicial?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pvp',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio de insumo'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.client'),
        ),
        migrations.CreateModel(
            name='IntoProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cant', models.IntegerField(default=0)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('into', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.into')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.product')),
            ],
            options={
                'verbose_name': 'Detalle de Entrada',
                'verbose_name_plural': 'Detalle de Entrada',
                'ordering': ['id'],
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='into',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pos.company'),
        ),
        migrations.AddField(
            model_name='client',
            name='cargo',
            field=models.ForeignKey(default=23, on_delete=django.db.models.deletion.PROTECT, to='pos.cargo', verbose_name='Cargo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='servicio',
            field=models.ForeignKey(default=23, on_delete=django.db.models.deletion.PROTECT, to='pos.servicio', verbose_name='Servicio a que Pertenece'),
            preserve_default=False,
        ),
    ]