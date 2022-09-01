import calendar
import json
import locale
import os

from re import template

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from weasyprint import HTML, CSS

from config import settings
from core.erp.forms import PayForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Pay, Sale, Client, Invoice, PayInvoice, PaySale, Zone


class PayListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'erp.view_pay'
    model = Pay
    template_name = 'pay/list.html'

    # locale.setlocale(locale.LC_TIME, "es_AR.utf8")
    locale.setlocale(locale.LC_TIME, "es_AR")

    # Ejemplo de filtro
    # def get_queryset(self):
    #     return Client.objects.filter(odorizador__price=600)

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                # se va a enviar los datos en un array para trabajar con datatables y ajax
                data = []
                # for i in PayInvoice.objects.all():
                #     item = i.toJSON()
                #     item['tipo'] = 'Factura'
                #     data.append(item)
                # for i in PaySale.objects.all():
                #     item = i.toJSON()
                #     item['tipo'] = 'Ventas'
                #     item['invoice'] = str(i.sale.id)
                #     data.append(item)
                for i in Pay.objects.all():
                    item = i.toJSON()
                    data.append(item)
            # elif action == 'view_zone_list':
            #     data = []
            #     for i in Client.objects.filter(zone_id=request.POST['id']):
            #         data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Planillas de cobranzas'
        context['create_url'] = reverse_lazy('erp:pay_create')
        context['list_url'] = reverse_lazy('erp:pay_list')
        context['entity'] = 'Cobranza'
        context['entity_pl'] = 'Cobranzas'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class PayCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'erp.add_pay'
    model = Pay
    form_class = PayForm
    template_name = 'pay/create.html'
    success_url = reverse_lazy('erp:pay_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                # con transaction.atomic si hay un error en algun campo no se guarda ningun dato
                with transaction.atomic():
                    # convierte el string a tipo json
                    vents = json.loads(request.POST['vents'])
                    # crea una instancia y guarda los datos de la factura
                    pay = Pay()
                    pay.date_pay = vents['date_pay']
                    pay.tecnic_id = vents['tecnic']
                    pay.total = float(vents['total'])
                    pay.zone_id = vents['zone']
                    pay.efectivo = vents['efectivo']
                    pay.cheque = vents['cheque']
                    pay.save()
                    # itera los items de la cobranza y los guarda en el detalle
                    for i in vents['products']:
                        if i['type'] == 'invoice':
                            payInvoice = PayInvoice()
                            payInvoice.pay_id = pay.id
                            payInvoice.invoice_id = i['id']
                            cli = i['cli']
                            payInvoice.cli_id = cli['id']
                            payInvoice.total = i['total']
                            payInvoice.save()
                        if i['type'] == 'sale':
                            paySale = PaySale()
                            paySale.pay_id = pay.id
                            paySale.sale_id = i['id']
                            cli = i['cli']
                            paySale.cli_id = cli['id']
                            paySale.total = i['total']
                            paySale.save()
                    data = {'id': pay.id}
            elif action == 'search_client':
                data = []
                # si es numerico busco por id
                if request.POST['term'].isnumeric():
                    prods = Client.objects.filter(id=request.POST['term'])
                # de lo contrario busco por nombre
                else:
                    prods = Client.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    # codigo para jquery ui
                    # item['value'] = i.name
                    # codigo para autocomplete de select2
                    item['text'] = i.name + " - " + i.address.capitalize()
                    data.append(item)
                # ordeno lista por orden alfabetico
                data = sorted(data, key=lambda cliente: cliente['text'])
            elif action == 'search_invoice_client':
                data = []
                # lista de todas las facturas y ventas del cliente
                prods = Invoice.objects.filter(cli_id=request.POST['id'])
                sales = Sale.objects.filter(cli_id=request.POST['id'])
                # itero facturas
                for i in prods:
                    # si no existe pago de la factura
                    if not PayInvoice.objects.filter(invoice_id=i.id):
                        item = i.toJSON()
                        # codigo para jquery ui
                        # item['value'] = i.name
                        # codigo para autocomplete de select2
                        item['text'] = 'Abono Nro: ', i.id, " (" + calendar.month_name[
                            i.date_joined.month] + ")", " ($" + str(i.total) + ")",
                        data.append(item)
                    # si existe sumo los pago de la misma factura
                    else:
                        pays = PayInvoice.objects.filter(invoice_id=i.id)
                        totalPays = 0
                        for pay in pays:
                            totalPays += pay.total
                        if i.total > totalPays:
                            i.total = i.total - totalPays
                            item = i.toJSON()
                            item['text'] = 'Abono Nro: ', i.id, " (" + calendar.month_name[
                                i.date_joined.month] + ")", " ($" + str(i.total) + ")",
                            data.append(item)
                # itero ventas
                for i in sales:
                    # si no existe pago de la venta
                    if not PaySale.objects.filter(sale_id=i.id):
                        item = i.toJSON()
                        item['text'] = 'Venta Nro: ', i.id
                        data.append(item)
                    # si existe sumo los pago de la misma venta
                    else:
                        pays = PaySale.objects.filter(sale_id=i.id)
                        totalPays = 0
                        for pay in pays:
                            totalPays += pay.total
                        if i.total > totalPays:
                            i.total = i.total - totalPays
                            item = i.toJSON()
                            item['text'] = 'Venta Nro: ', i.id
                            data.append(item)
            elif action == 'search_zone_id':
                data = []
                zones = Zone.objects.filter(tecnic_id=request.POST['id'])
                for i in zones:
                    item = {}
                    item['id'] = i.id
                    item['name'] = i.name
                    data.append(item)
                print(data)
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Carga de Cobranza '
        context['entity'] = 'Cobranza'
        context['entity_pl'] = 'Cobranzas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class PayUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = 'erp.change_pay'
    model = Pay
    form_class = PayForm
    template_name = 'pay/create.html'
    success_url = reverse_lazy('erp:pay_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                # con transaction.atomic si hay un error en algun campo no se guarda ningun dato
                with transaction.atomic():
                    # convierte el string a tipo json
                    vents = json.loads(request.POST['vents'])
                    # edita una instancia y guarda los datos de la factura
                    pay = Pay.objects.filter(id=kwargs['pk']).first()
                    pay.date_pay = vents['date_pay']
                    pay.tecnic_id = vents['tecnic']
                    pay.total = float(vents['total'])
                    pay.zone_id = vents['zone']
                    pay.efectivo = vents['efectivo']
                    pay.cheque = vents['cheque']
                    pay.save()
                    # Elimina los registros anteriores
                    PayInvoice.objects.filter(pay_id=pay.id).delete()
                    PaySale.objects.filter(pay_id=pay.id).delete()
                    # itera los productos de la factura y los guarda en el detalle
                    for i in vents['products']:
                        if i['type'] == 'invoice':
                            payInvoice = PayInvoice()
                            payInvoice.pay_id = pay.id
                            payInvoice.invoice_id = i['invoice_id']
                            cli = i['cli']
                            payInvoice.cli_id = cli['id']
                            payInvoice.total = i['total']
                            payInvoice.save()
                        if i['type'] == 'sale':
                            paySale = PaySale()
                            paySale.pay_id = pay.id
                            paySale.sale_id = i['sale_id']
                            cli = i['cli']
                            paySale.cli_id = cli['id']
                            paySale.total = i['total']
                            paySale.save()
                    data = {'id': pay.id}
            elif action == 'search_client':
                data = []
                # si es numerico busco por id
                if request.POST['term'].isnumeric():
                    prods = Client.objects.filter(id=request.POST['term'])
                # de lo contrario busco por nombre
                else:
                    prods = Client.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    # codigo para jquery ui
                    # item['value'] = i.name
                    # codigo para autocomplete de select2
                    item['text'] = i.name + " - " + i.address.capitalize()
                    data.append(item)
                # ordeno lista por orden alfabetico
                data = sorted(data, key=lambda cliente: cliente['text'])
            elif action == 'search_invoice_client':
                data = []
                # lista de todas las facturas y ventas del cliente
                prods = Invoice.objects.filter(cli_id=request.POST['id'])
                sales = Sale.objects.filter(cli_id=request.POST['id'])
                # itero facturas
                for i in prods:
                    # si no existe pago de la factura
                    if not PayInvoice.objects.filter(invoice_id=i.id):
                        item = i.toJSON()
                        # codigo para jquery ui
                        # item['value'] = i.name
                        # codigo para autocomplete de select2
                        item['text'] = 'Abono Nro: ', i.id, " (" + calendar.month_name[
                            i.date_joined.month] + ")", " ($" + str(i.total) + ")",
                        data.append(item)
                    # si existe sumo los pago de la misma factura
                    else:
                        pays = PayInvoice.objects.filter(invoice_id=i.id)
                        totalPays = 0
                        for pay in pays:
                            totalPays += pay.total
                        if i.total > totalPays:
                            i.total = i.total - totalPays
                            item = i.toJSON()
                            item['text'] = 'Abono Nro: ', i.id
                            data.append(item)
                # itero ventas
                for i in sales:
                    # si no existe pago de la venta
                    if not PaySale.objects.filter(sale_id=i.id):
                        item = i.toJSON()
                        item['text'] = 'Venta Nro: ', i.id
                        data.append(item)
                    # si existe sumo los pago de la misma venta
                    else:
                        pays = PaySale.objects.filter(sale_id=i.id)
                        totalPays = 0
                        for pay in pays:
                            totalPays += pay.total
                        if i.total > totalPays:
                            i.total = i.total - totalPays
                            item = i.toJSON()
                            item['text'] = 'Venta Nro: ', i.id
                            data.append(item)
            elif action == 'init_edit':
                data = []
                pay = PayInvoice.objects.filter(pay_id=kwargs['pk'])
                sales = PaySale.objects.filter(pay_id=kwargs['pk'])
                for i in pay:
                    print(i.toJSON())
                    j = Invoice.objects.filter(id=i.invoice_id).first()
                    item = j.toJSON()
                    data.append(item)
                for i in sales:
                    j = Sale.objects.filter(id=i.sale_id).first()
                    item = j.toJSON()
                    data.append(item)
                print(data)
            elif action == 'search_zone_id':
                data = []
                zones = Zone.objects.filter(tecnic_id=request.POST['id'])
                for i in zones:
                    item = {}
                    item['id'] = i.id
                    item['name'] = i.name
                    data.append(item)
                print(data)
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = ' Edición de una cobranza '
        context['entity'] = 'Cobranza'
        context['entity_pl'] = 'Cobranzas'
        context['list_url'] = reverse_lazy('erp:pay_list')
        context['action'] = 'edit'
        return context


class PayDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = 'erp.delete_pay'
    model = Pay
    template_name = 'pay/delete.html'
    success_url = reverse_lazy('erp:pay_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            for i in PayInvoice.objects.filter(pay_id=kwargs['pk']):
                i.delete()
            for i in PaySale.objects.filter(pay_id=kwargs['pk']):
                i.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Eliminación de una cobranza '
        context['entity'] = 'Cobranza'
        context['entity_pl'] = 'Cobranzas'
        context['list_url'] = reverse_lazy('erp:pay_list')
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class PayPrintPdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            # pay = Pay.objects.get(pk=self.kwargs['pk']).firts()
            # id = pay.id
            template = get_template('pay/print_pays.html')
            context = {
                'title': 'Cobranza',
                'pay': Pay.objects.get(pk=self.kwargs['pk']),
                # 'invoice': Invoice.objects.filter(payinvoice__pay_id=id),
                # 'sale': Sale.objects.filter(paysale__pay_id=id),
                'comp': {'name': 'SoftGestion',
                         'cuit': '11-11111111-1',
                         'address': 'Rosario, Sta Fe, Argentina',
                         'phone': '341-3112233',
                         'web': 'softgestion.com'
                         },
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo2.png')
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:pay_list'))


# test
class PayCreateViewTest(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'erp.add_pay'
    model = Pay
    form_class = PayForm
    template_name = 'pay/create_test.html'
    success_url = reverse_lazy('erp:pay_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                # con transaction.atomic si hay un error en algun campo no se guarda ningun dato
                with transaction.atomic():
                    # convierte el string a tipo json
                    vents = json.loads(request.POST['vents'])
                    # crea una instancia y guarda los datos de la factura
                    pay = Pay()
                    pay.date_pay = vents['date_pay']
                    pay.tecnic_id = vents['tecnic']
                    pay.total = float(vents['total'])
                    pay.zone_id = vents['zone']
                    pay.efectivo = vents['efectivo']
                    pay.cheque = vents['cheque']
                    pay.save()
                    # itera los items de la cobranza y los guarda en el detalle
                    for i in vents['products']:
                        if i['type'] == 'invoice':
                            payInvoice = PayInvoice()
                            payInvoice.pay_id = pay.id
                            payInvoice.invoice_id = i['id']
                            cli = i['cli']
                            payInvoice.cli_id = cli['id']
                            payInvoice.total = i['total']
                            payInvoice.save()
                        if i['type'] == 'sale':
                            paySale = PaySale()
                            paySale.pay_id = pay.id
                            paySale.sale_id = i['id']
                            cli = i['cli']
                            paySale.cli_id = cli['id']
                            paySale.total = i['total']
                            paySale.save()
                    data = {'id': pay.id}
            elif action == 'search_client':
                data = []
                # si es numerico busco por id
                if request.POST['term'].isnumeric():
                    prods = Client.objects.filter(id=request.POST['term'])
                # de lo contrario busco por nombre
                else:
                    prods = Client.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    # codigo para jquery ui
                    # item['value'] = i.name
                    # codigo para autocomplete de select2
                    item['text'] = i.name + " - " + i.address.capitalize()
                    data.append(item)
                # ordeno lista por orden alfabetico
                data = sorted(data, key=lambda cliente: cliente['text'])
            elif action == 'search_invoice_client':
                data = []
                # lista de todas las facturas y ventas del cliente
                prods = Invoice.objects.filter(cli_id=request.POST['id'])
                sales = Sale.objects.filter(cli_id=request.POST['id'])
                # itero facturas
                for i in prods:
                    # si no existe pago de la factura
                    if not PayInvoice.objects.filter(invoice_id=i.id):
                        item = i.toJSON()
                        # codigo para jquery ui
                        # item['value'] = i.name
                        # codigo para autocomplete de select2
                        item['text'] = 'Abono Nro: ', i.id, " (" + calendar.month_name[
                            i.date_joined.month] + ")", " ($" + str(i.total) + ")",
                        data.append(item)
                    # si existe sumo los pago de la misma factura
                    else:
                        pays = PayInvoice.objects.filter(invoice_id=i.id)
                        totalPays = 0
                        for pay in pays:
                            totalPays += pay.total
                        if i.total > totalPays:
                            i.total = i.total - totalPays
                            item = i.toJSON()
                            item['text'] = 'Abono Nro: ', i.id, " (" + calendar.month_name[
                                i.date_joined.month] + ")", " ($" + str(i.total) + ")",
                            print(item['text'])
                            data.append(item)
                # itero ventas
                for i in sales:
                    # si no existe pago de la venta
                    if not PaySale.objects.filter(sale_id=i.id):
                        item = i.toJSON()
                        item['text'] = 'Venta Nro: ', i.id
                        data.append(item)
                    # si existe sumo los pago de la misma venta
                    else:
                        pays = PaySale.objects.filter(sale_id=i.id)
                        totalPays = 0
                        for pay in pays:
                            totalPays += pay.total
                        if i.total > totalPays:
                            i.total = i.total - totalPays
                            item = i.toJSON()
                            item['text'] = 'Venta Nro: ', i.id
                            data.append(item)
            elif action == 'search_invoice_id':
                data = []
                id = request.POST['id']
                # lista de todas las facturas y ventas del cliente
                invoice = Invoice.objects.filter(id=id).first()

                if invoice == None:
                    data = {}
                    data['error'] = 'No se encontro el codigo ingresado'
                    return JsonResponse(data, safe=False)

                if not PayInvoice.objects.filter(invoice_id=id):
                    invoice = invoice.toJSON()
                    data.append(invoice)
                else:
                    pays = PayInvoice.objects.filter(invoice_id=id)
                    totalPays = 0
                    for pay in pays:
                        totalPays += pay.total
                    if invoice.total > totalPays:
                        invoice.total = invoice.total - totalPays
                        invoice = invoice.toJSON()
                        data.append(invoice)
                    else:
                        data = {}
                        data['error'] = 'El recibo ya fue abonado'
            elif action == 'search_zone_id':
                data = []
                zones = Zone.objects.filter(tecnic_id=request.POST['id'])
                for i in zones:
                    item = {}
                    item['id'] = i.id
                    item['name'] = i.name
                    data.append(item)
                print(data)
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Carga de Cobranza '
        context['entity'] = 'Cobranza'
        context['entity_pl'] = 'Cobranzas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context
