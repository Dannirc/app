import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DeleteView, View

from core.erp.forms import InvoiceForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Sale, Invoice, DetInvoice, Client, Services, PayInvoice, Tecnic, Zone

from weasyprint import HTML, CSS


class InvoiceListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'erp.view_invoice'
    model = Invoice
    template_name = 'invoice/list.html'

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
                # guardo fecha en string
                date_start = request.POST['date_start']
                date_end = request.POST['date_end']
                # convierto fecha datetime.date
                fecha_desde = datetime.strptime(date_start, '%Y-%m-%d').date()
                fecha_hasta = datetime.strptime(date_end, '%Y-%m-%d').date()
                for i in Invoice.objects.filter(date_joined__gte=fecha_desde, date_joined__lte=fecha_hasta):
                    # compruebo si esta oaga la factura
                    payed = False
                    if PayInvoice.objects.filter(invoice_id=i.id):
                        payed = True
                    dict = i.toJSON()
                    dict['payed'] = payed
                    # envio las facturas al data
                    data.append(dict)
            elif action == 'search_details_service':
                data = []
                for i in DetInvoice.objects.filter(invoice_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Facturas'
        context['create_url'] = reverse_lazy('erp:invoice_create')
        context['list_url'] = reverse_lazy('erp:invoice_list')
        context['entity'] = 'Factura'
        context['entity_pl'] = 'Facturas'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class InvoiceCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'erp.add_invoice'
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoice/create.html'
    success_url = reverse_lazy('erp:invoice_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        iva = 0
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                serv = Services.objects.filter(cli_id=request.POST['id'])
                for i in serv:
                    item = i.toJSON()
                    # codigo para jquery ui
                    # item['value'] = i.name
                    # codigo para autocomplete de select2
                    item['text'] = i.name
                    item['subtotal'] = i.odorizador.price * i.cant_odo
                    data.append(item)
            if action == 'add':
                # Factura el cliente seleccionado
                if request.POST['cli'] != '0':
                    invoice = Invoice()
                    det = DetInvoice()
                    cli = Client.objects.filter(id=request.POST['cli']).first()
                    service = Services.objects.filter(cli_id=request.POST['cli']).first()

                    invoice.cli = cli
                    invoice.date_joined = datetime.now()
                    invoice.type = 'invoice'

                    if service.odorizador is not None:
                        det.price_odo = service.odorizador.price
                        det.cant_odo = service.cant_odo
                    if service.aerosoles is not None:
                        det.price_aer = service.aerosoles.price
                        det.cant_aer = service.cant_aer
                    if service.goteos is not None:
                        det.price_got = service.goteos.price
                        det.cant_got = service.cant_got
                    det.subtotal = det.price_odo * det.cant_odo + det.price_aer * det.cant_aer + det.price_got * det.cant_got

                    if det.subtotal > 0:
                        invoice.subtotal = det.subtotal
                        invoice.total = det.subtotal + det.subtotal * iva
                        invoice.save()
                        det.invoice_id = invoice.id
                        det.save()

                    data = {'id': 'Clientes Facturados'}
                # Factura todos los clientes habilitados y activos
                elif request.POST['select_tecnic'] == '0':
                    clients = Client.objects.filter(enable=True, active=True)

                    for cli in clients:
                        invoice = Invoice()
                        det = DetInvoice()
                        service = Services.objects.filter(cli_id=cli.id).first()

                        invoice.cli = cli
                        invoice.date_joined = datetime.now()
                        invoice.type = 'invoice'

                        if service.odorizador is not None:
                            det.price_odo = service.odorizador.price
                            det.cant_odo = service.cant_odo
                        else:
                            det.price_odo = 0
                            det.cant_odo = 0
                        if service.aerosoles is not None:
                            det.price_aer = service.aerosoles.price
                            det.cant_aer = service.cant_aer
                        else:
                            det.price_aer = 0
                            det.cant_aer = 0
                        if service.goteos is not None:
                            det.price_got = service.goteos.price
                            det.cant_got = service.cant_got
                        else:
                            det.price_got = 0
                            det.cant_got = 0
                        det.subtotal = det.price_odo * det.cant_odo + det.price_aer * det.cant_aer + det.price_got * det.cant_got

                        if det.subtotal > 0:
                            invoice.subtotal = det.subtotal
                            invoice.total = det.subtotal + det.subtotal * iva
                            invoice.save()
                            det.invoice_id = invoice.id
                            det.save()

                    data = {'id': 'Clientes Facturados'}
                # Factura Todos los clientes habilitados y activos del tecnico seleccionado
                elif request.POST['select_zone'] == '0':
                    clients = Client.objects.filter(tecnic_id=request.POST['select_tecnic']).filter(enable=True, active=True)
                    for cli in clients:
                        invoice = Invoice()
                        det = DetInvoice()
                        service = Services.objects.filter(cli_id=cli.id).first()

                        invoice.cli = cli
                        invoice.date_joined = datetime.now()
                        invoice.type = 'invoice'

                        if service.odorizador is not None:
                            det.price_odo = service.odorizador.price
                            det.cant_odo = service.cant_odo
                        else:
                            det.price_odo = 0
                            det.cant_odo = 0
                        if service.aerosoles is not None:
                            det.price_aer = service.aerosoles.price
                            det.cant_aer = service.cant_aer
                        else:
                            det.price_aer = 0
                            det.cant_aer = 0
                        if service.goteos is not None:
                            det.price_got = service.goteos.price
                            det.cant_got = service.cant_got
                        else:
                            det.price_got = 0
                            det.cant_got = 0
                        det.subtotal = det.price_odo * det.cant_odo + det.price_aer * det.cant_aer + det.price_got * det.cant_got

                        if det.subtotal > 0:
                            invoice.subtotal = det.subtotal
                            invoice.total = det.subtotal + det.subtotal * iva
                            invoice.save()
                            det.invoice_id = invoice.id
                            det.save()

                    data = {'id': 'Clientes Facturados'}
                # Factura todos los clientes habilitados y activos de la zona seleccionada
                else:
                    clients = Client.objects.filter(zone_id=request.POST['select_zone']).filter(enable=True, active=True)
                    for cli in clients:
                        invoice = Invoice()
                        det = DetInvoice()
                        service = Services.objects.filter(cli_id=cli.id).first()

                        invoice.cli = cli
                        invoice.date_joined = datetime.now()
                        invoice.type = 'invoice'

                        if service.odorizador is not None:
                            det.price_odo = service.odorizador.price
                            det.cant_odo = service.cant_odo
                        else:
                            det.price_odo = 0
                            det.cant_odo = 0
                        if service.aerosoles is not None:
                            det.price_aer = service.aerosoles.price
                            det.cant_aer = service.cant_aer
                        else:
                            det.price_aer = 0
                            det.cant_aer = 0
                        if service.goteos is not None:
                            det.price_got = service.goteos.price
                            det.cant_got = service.cant_got
                        else:
                            det.price_got = 0
                            det.cant_got = 0
                        det.subtotal = det.price_odo * det.cant_odo + det.price_aer * det.cant_aer + det.price_got * det.cant_got

                        if det.subtotal > 0:
                            invoice.subtotal = det.subtotal
                            invoice.total = det.subtotal + det.subtotal * iva
                            invoice.save()
                            det.invoice_id = invoice.id
                            det.save()

                    data = {'id': 'Clientes Facturados'}
            # actions para completar los selects en el form
            # devuelve los tecnicos
            elif action == 'search_tecnic':
                data = []
                for i in Tecnic.objects.all():
                    tecnic = i.toJSON()
                    data.append(tecnic)
            # devuelve zonas pertenecientes al tecnico seleccionado
            elif action == 'search_zone':
                data = []
                for i in Zone.objects.filter(tecnic_id=request.POST['id']):
                    zone = i.toJSON()
                    data.append(zone)
            # devuelve lista de clientes segun parametros solicitados
            elif action == 'search_client':
                data = []
                # devuelve todos los clientes habilitados
                if request.POST['tecnic_id'] == '0' and request.POST['zone_id'] == '0':
                    for i in Client.objects.filter(enable=True, active=True):
                        zone = i.toJSON()
                        data.append(zone)
                # devuelve todos los clientes habilitados del tecnico seleccionado
                elif request.POST['zone_id'] == '0':
                    for i in Client.objects.filter(tecnic_id=request.POST['tecnic_id']).filter(enable=True, active=True):
                        zone = i.toJSON()
                        data.append(zone)
                # devuelve todos los clientes habilitados de la zona seleccionada
                else:
                    for i in Client.objects.filter(zone_id=request.POST['zone_id']).filter(enable=True, active=True):
                        zone = i.toJSON()
                        data.append(zone)
                data = sorted(data, key=lambda client : client['name'])
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Creación de una Factura '
        context['entity'] = 'Factura'
        context['entity_pl'] = 'Facturas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['date_now'] = datetime.now()
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class InvoiceDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = 'erp.delete_invoice'
    model = Invoice
    template_name = 'invoice/delete.html'
    success_url = reverse_lazy('erp:invoice_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Eliminación de una factura '
        context['entity'] = 'Factura'
        context['entity_pl'] = 'Facturas'
        context['list_url'] = reverse_lazy('erp:invoice_list')
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class InvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('invoice/invoice.html')
            context = {
                'title': 'Factura de Servicios',
                'invoice': Invoice.objects.get(pk=self.kwargs['pk']),
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
