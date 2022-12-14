from datetime import datetime

from django.db import models
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from config import settings
from core.pos.choices import genders


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

class Cargo(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['id']

class Servicio(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre del Servicio', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['id']

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    is_inventoried = models.BooleanField(default=True, verbose_name='¿Es invetario inicial?')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de insumo')

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.__str__()
        item['category'] = self.category.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = f'{self.pvp:.2f}'
        return item

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']
class Company(models.Model):
    name = models.CharField(max_length=150, verbose_name='Centro de Salud')
    ruc = models.CharField(max_length=13, verbose_name='NIT')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    mobile = models.CharField(max_length=8, verbose_name='Teléfono Institucional')
    phone = models.CharField(max_length=8, verbose_name='Teléfono Fax')
    website = models.CharField(max_length=150, verbose_name='Website')
    image = models.ImageField(upload_to='company/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Compañia'
        verbose_name_plural = 'Compañias'
        default_permissions = ()
        permissions = (
            ('change_company', 'Can change Company'),
        )
        ordering = ['id']
class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, verbose_name='Servicio a que Pertenece')
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, verbose_name='Cargo')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=genders, default='male', verbose_name='Genero')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.names} ({self.servicio})'

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['servicio'] = self.servicio.toJSON()
        item['cargo'] = self.cargo.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()

        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Into(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True)
    date_joined = models.DateField(default=datetime.now)
    requisicion = models.IntegerField( null= True, verbose_name="No_requisicion" )
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if Company.objects.all().exists():
            self.company = Company.objects.first()
        super(Into, self).save()
    def __str__(self):
        return self.requisicion
    def get_number(self):
        return f'{self.id:06d}'

    def toJSON(self):
        item = model_to_dict(self)
        item['number'] = self.get_number()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['requisicion'] = self.requisicion
        item['subtotal'] = f'{self.subtotal:.2f}'
        item['intoproduct'] = [i.toJSON() for i in self.intoproduct_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for detail in self.intoproduct_set.filter(product__is_inventoried=True):
            detail.product.stock += detail.cant
            detail.product.save()
        super(Into, self).delete()

    def calculate_invoice(self):
        subtotal = self.intoproduct_set.all().aggregate(result=Coalesce(Sum(F('price') * F('cant')), 0.00, output_field=FloatField())).get('result')
        self.subtotal = subtotal
        # self.total_iva = self.subtotal * float(self.iva)
        # self.total = float(self.subtotal) + float(self.total_iva)
        self.save()

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'
        ordering = ['id']


class IntoProduct(models.Model):
    into = models.ForeignKey(Into, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['into'])
        item['product'] = self.product.toJSON()
        item['price'] = f'{self.price:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Entrada'
        verbose_name_plural = 'Detalle de Entrada'
        default_permissions = ()
        ordering = ['id']

class Sale(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    requisicion = models.CharField(max_length=10, unique=True, verbose_name='No Requisicion')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    # iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    # total_iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    # total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.client.names

    def __str__(self):
        return self.requisicion

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if Company.objects.all().exists():
            self.company = Company.objects.first()
        super(Sale, self).save()

    def get_number(self):
        return f'{self.id:06d}'

    def toJSON(self):
        item = model_to_dict(self)
        item['number'] = self.get_number()
        item['client'] = self.client.toJSON()
        item['subtotal'] = f'{self.subtotal:.2f}'
        # item['iva'] = f'{self.iva:.2f}'
        # item['total_iva'] = f'{self.total_iva:.2f}'
        # item['total'] = f'{self.total:.2f}'
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['saleproduct'] = [i.toJSON() for i in self.saleproduct_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for detail in self.saleproduct_set.filter(product__is_inventoried=True):
            detail.product.stock += detail.cant
            detail.product.save()
        super(Sale, self).delete()

    def calculate_invoice(self):
        subtotal = self.saleproduct_set.all().aggregate(result=Coalesce(Sum(F('price') * F('cant')), 0.00, output_field=FloatField())).get('result')
        self.subtotal = subtotal
        # self.total_iva = self.subtotal * float(self.iva)
        # self.total = float(self.subtotal) + float(self.total_iva)
        self.save()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = f'{self.price:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Solicitud'
        verbose_name_plural = 'Detalle de Solicitudes'
        default_permissions = ()
        ordering = ['id']
