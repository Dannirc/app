from datetime import datetime

from crum import get_current_user
from django.utils import timezone

from config.settings import MEDIA_URL, STATIC_URL
from django.db import models
from django.forms import model_to_dict

from core.models import BaseModel

import locale
# locale.setlocale(locale.LC_TIME, 'es-AR')


class Abono(models.Model):
    choices_type_abono = (('Od', 'Odorizador'), ('Ae', 'Aerosol'), ('Go', 'Goteo'))

    name = models.CharField(max_length=50, verbose_name='Nombre del Abono')
    type = models.CharField(choices=choices_type_abono, max_length=2, default='Od', null=True, blank=True, verbose_name='Tipo Abono')
    price = models.FloatField(default=0.00, verbose_name='Precio del Abono')
    description = models.CharField(max_length=200, verbose_name='Descripción del Abono', null=True, blank=True)
    date_created = models.DateField(editable=False, verbose_name='Fecha Creación de Abono')
    date_updated = models.DateField(verbose_name='Fecha Actualización de Abono')

    def __str__(self):
        return self.name

    def toJSON(self):
        # convierte todos los campos de el objeto en un diccionario y los asigna a la variable
        item = model_to_dict(self)
        item['price'] = format(self.price, '.2f')
        item['type'] = self.get_type_display()
        item['date_created'] = self.date_created.strftime('%d/%m/%y').capitalize()
        item['date_updated'] = self.date_updated.strftime('%d/%m/%y').capitalize()
        return item

    class Meta:
        verbose_name = 'Abono'
        verbose_name_plural = 'Abonos'
        ordering = ['id']

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date_created = timezone.now()
        self.date_updated = timezone.now()
        return super(Abono, self).save(*args, **kwargs)


class Tecnic(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Nombre Tecnico')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        # convierte todos los campos de el objeto en un diccionario y los asigna a la variable
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tecnico'
        verbose_name_plural = 'Tecnicos'
        ordering = ['id']


class Zone(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre de la zona')
    tecnic = models.ForeignKey(Tecnic, on_delete=models.CASCADE, verbose_name='Nombre del Tecnico', blank=True, null=True,)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    dateWork = models.DateField(default=datetime.now, verbose_name="Fecha de realizacion")
    enable = models.BooleanField(default=True, verbose_name='Habilitado')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['tecnic'] = self.tecnic.toJSON()
        return item

    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'
        ordering = ['id']


class Client(BaseModel):
    choices_type_pay = (('Ef', 'Efectivo'), ('Tr', 'Transferencia'), ('Ch', 'Cheque'))

    name = models.CharField(max_length=150, verbose_name='Nombre o Razon Social')
    cuit = models.CharField(max_length=11, null=True, blank=True, verbose_name='Cuit')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Domicilio')
    address_invoice = models.CharField(max_length=150, null=True, blank=True, verbose_name='Domicilio Factura')
    phone = models.CharField(max_length=150, null=True, blank=True, verbose_name='Telefono')
    contact = models.CharField(max_length=150, null=True, blank=True, verbose_name='Nombre de Contacto')
    email = models.EmailField(null=True, blank=True, verbose_name='Correo Electronico')
    schedule = models.CharField(max_length=150, null=True, blank=True, verbose_name='Horario')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    type_pay = models.CharField(choices=choices_type_pay, max_length=2, default='Ef', null=True, blank=True, verbose_name='Tipo_pago')
    tecnic = models.ForeignKey(Tecnic, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Nombre de Tecnico', default=1)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Nombre de Zona', default=1)
    position = models.IntegerField(default=99, null=True, blank=True, verbose_name='Posicion')
    enable = models.BooleanField(default=True, verbose_name='Habilitado')
    active = models.BooleanField(default=True, verbose_name='Activado')
    # falta agregar cliente a una empresa (se implementara igual que services, con betterform)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Client, self).save()

    def toJSON(self):
        # convierte todos los campos de el objeto en un diccionario y los asigna a la variable
        item = model_to_dict(self, exclude=['user_creation', 'user_update'])
        item['tecnic'] = self.tecnic.toJSON()
        if self.zone:
            item['zone'] = self.zone.toJSON()
        else:
            item['zone'] = {"name": "N/A"}
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Services(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Nombre de cliente')
    odorizador = models.ForeignKey(Abono, related_name='related_odorizador_abono',  on_delete=models.SET_NULL, verbose_name='Abono Odorizador', blank=True, null=True)
    cant_odo = models.IntegerField(default=0, verbose_name='Cantidad Odorizadores')
    aerosoles = models.ForeignKey(Abono, related_name='related_aerosoles_abono', on_delete=models.SET_NULL, verbose_name='Abono Aerosoles', blank=True, null=True)
    cant_aer = models.IntegerField(default=0, verbose_name='Cantidad Aerosoles')
    goteos = models.ForeignKey(Abono, related_name='related_goteos_abono', on_delete=models.SET_NULL, verbose_name='Abono Goteos', blank=True, null=True)
    cant_got = models.IntegerField(default=0, verbose_name='Cantidad Goteos')

    def __str__(self):
        return self.cli.name

    def toJSON(self):
        # convierte todos los campos de el objeto en un diccionario y los asigna a la variable
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        if self.odorizador:
            item['odorizador'] = self.odorizador.toJSON()
        if self.aerosoles:
            item['aerosoles'] = self.aerosoles.toJSON()
        if self.goteos:
            item['goteos'] = self.goteos.toJSON()
        return item

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['id']


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


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cat'] = self.cat.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Invoice(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Factura')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    type = models.CharField(max_length=20, verbose_name='Tipo')

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%B %y').capitalize()
        # lo utilizo para poder llamarlo desde la funcion format en el datatable de la venta y mostrarlo en "child row"
        item['det'] = [i.toJSON() for i in self.detinvoice_set.all()]
        item['type'] = self.type
        item['invoice_id'] = self.id
        return item

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['id']


class DetInvoice(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    price_odo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant_odo = models.IntegerField(default=0)
    price_aer = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant_aer = models.IntegerField(default=0)
    price_got = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant_got = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.invoice.date_joined.strftime("%m-%Y")

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['price_odo'] = format(self.price_odo, '.2f')
        item['price_aer'] = format(self.price_aer, '.2f')
        item['price_got'] = format(self.price_got, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Factura'
        verbose_name_plural = 'Detalle de Facturas'
        ordering = ['id']


class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    type = models.CharField(max_length=20, verbose_name='Tipo')

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        # lo utilizo para poder llamarlo desde la funcion format en el datatable de la venta y mostrarlo en "child row"
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        item['sale_id'] = self.id
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']


class Pay(models.Model):
    tecnic = models.ForeignKey(Tecnic, on_delete=models.CASCADE, verbose_name="Cobrador", null=True, blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, verbose_name="Zona realizada", null=True, blank=True)
    date_pay = models.DateField(default=datetime.now, verbose_name="Fecha de Pago")
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name="Total cobrado")
    efectivo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name="Efectivo", null=True, blank=True)
    cheque = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name="Cheque", null=True, blank=True)

    def __str__(self):
        return self.total

    def toJSON(self):
        # convierte todos los campos de el objeto en un diccionario y los asigna a la variable
        item = model_to_dict(self)
        item['tecnic'] = self.tecnic.toJSON()
        item['date_pay'] = self.date_pay.strftime('%d/%m/%y')
        return item

    class Meta:
        verbose_name = 'Cobranza'
        verbose_name_plural = 'Cobranzas'
        ordering = ['id']


class PayInvoice(models.Model):
    pay = models.ForeignKey(Pay, on_delete=models.CASCADE, verbose_name="Cobranza Id")
    cli = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente")
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name="Factura cobrada")
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name="Total")

    def __str__(self):
        return self.total

    def toJSON(self):
        # convierte todos los campos de el objeto en un diccionario y los asigna a la variable
        item = model_to_dict(self)
        item['pay'] = self.pay.toJSON()
        item['cli'] = self.cli.toJSON()
        item['invoice'] = self.invoice.id
        item['total'] = format(self.total, '.2f')
        item['type'] = self.invoice.type
        return item

    class Meta:
        verbose_name = 'Cobro de factura'
        verbose_name_plural = 'Cobros de factura'
        ordering = ['id']


class PaySale(models.Model):
    pay = models.ForeignKey(Pay, on_delete=models.CASCADE, verbose_name="Cobranza Id")
    cli = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente")
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name="Id de Venta")
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name="Total")

    def __str__(self):
        return self.total

    def toJSON(self):
        # convierte todos los campos de el objeto en un diccionario y los asigna a la variable
        item = model_to_dict(self)
        item['pay'] = self.pay.toJSON()
        item['cli'] = self.cli.toJSON()
        item['sale'] = self.sale.id
        item['total'] = format(self.total, '.2f')
        item['type'] = self.sale.type
        return item

    class Meta:
        verbose_name = 'Cobro de Venta'
        verbose_name_plural = 'Cobros de ventas'
        ordering = ['id']


class ClientPending(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente pendiente id")
    date = models.DateField(default=datetime.now, verbose_name="Fecha de pendiente")
    dateToMake = models.DateField(blank=True, null=True, verbose_name="Fecha a realizar")
    dateRealized = models.DateField(blank=True, null=True, verbose_name="Fecha realizado")
    observation = models.CharField(max_length=200, blank=True, null=True, verbose_name='Motivo')

    def __str__(self):
        return self.cli.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['date'] = self.date.strftime("%d/%m/%y")
        if self.dateToMake != None:
            item['dateToMake'] = self.dateToMake.strftime("%d/%m/%y")
        item['dateRealized'] = self.dateRealized
        item['observation'] = self.observation
        return item

    class Meta:
        verbose_name = 'Cliente Pendiente'
        verbose_name_plural = 'Clientes Pendientes'
        ordering = ['id']


class JobTecnic(models.Model):
    tecnic = models.ForeignKey(Tecnic, on_delete=models.CASCADE, verbose_name= "Tecnico")
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Zona")
    date = models.DateField(default=datetime.now, verbose_name="Fecha del trabajo")
    cantEquipos = models.IntegerField(blank=True, null=True, verbose_name="Cantidad de equipos realizados")
    cantClient = models.IntegerField(blank=True, null=True, verbose_name="Cantidad de clientes realizados")
    totalFact = models.IntegerField(blank=True, null=True, verbose_name="Total Facturado $")

    def __str__(self):
        return self.tecnic.name

    def toJSON(self):
        item = model_to_dict(self)
        item['tecnic'] = self.tecnic.toJSON()
        item['zone'] = self.zone.toJSON()
        item['date'] = self.date
        item['cantEquipos'] = self.cantEquipos
        item['cantClient'] = self.cantClient
        item['totalFact'] = self.totalFact
        return item

    class Meta:
        verbose_name = 'Cliente Pendiente'
        verbose_name_plural = 'Clientes Pendientes'
        ordering = ['id']


class EquipRemove(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente")
    date = models.DateField(default=datetime.now, verbose_name="Fecha de Retiro")
    cantOdo = models.IntegerField(blank=True, null=True, verbose_name="Cantidad de odorizadores retirados")
    cantAer = models.IntegerField(blank=True, null=True, verbose_name="Cantidad de aerosoles retirados")
    cantGot = models.IntegerField(blank=True, null=True, verbose_name="Cantidad de goteos retirados")

    def __str__(self):
        return self.cli.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['date'] = self.date
        item['cantOdo'] = self.cantOdo
        item['cantAer'] = self.cantAer
        item['cantGot'] = self.cantGot
        return item

    class Meta:
        verbose_name = 'Cliente Retirado'
        verbose_name_plural = 'Clientes Retirados'
        ordering = ['id']


class EquipSuspend(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente")
    date = models.DateField(default=datetime.now, verbose_name="Fecha de Suspensión")
    date_end = models.DateField(blank=True, null=True, verbose_name="Fecha de Reactivación")
    cantOdo = models.IntegerField(blank=True, null=True, verbose_name="Cantidad de odorizadores suspendidos")
    cantAer = models.IntegerField(blank=True, null=True, verbose_name="Cantidad de aerosoles suspendidos")
    cantGot = models.IntegerField(blank=True, null=True, verbose_name="Cantidad de goteos suspendidos")

    def __str__(self):
        return self.cli.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['date'] = self.date
        item['date_end'] = self.date_end
        item['cantOdo'] = self.cantOdo
        item['cantAer'] = self.cantAer
        item['cantGot'] = self.cantGot
        return item

    class Meta:
        verbose_name = 'Cliente Suspendido'
        verbose_name_plural = 'Clientes Suspendidos'
        ordering = ['id']