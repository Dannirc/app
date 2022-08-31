import json
import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DeleteView, View

from core.erp.forms import SaleForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Sale, Product, DetSale, PaySale

from weasyprint import HTML, CSS


class SaleListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'erp.view_sale'
    model = Sale
    template_name = 'sale/list.html'

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
                for i in Sale.objects.all():
                    # compruebo si esta paga la venta
                    payed = False
                    if PaySale.objects.filter(sale_id=i.id):
                        payed = True
                    dict = i.toJSON()
                    dict['payed'] = payed
                    # envio las facturas al data
                    data.append(dict)
            elif action == 'search_details_prod':
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('erp:sale_create')
        context['list_url'] = reverse_lazy('erp:sale_list')
        context['entity'] = 'Venta'
        context['entity_pl'] = 'Ventas'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class SaleCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'erp.add_sale'
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('erp:sale_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    # codigo para jquery ui
                    # item['value'] = i.name
                    # codigo para autocomplete de select2
                    item['text'] = i.name
                    data.append(item)
            elif action == 'add':
                # con transaction.atomic si hay un error en algun campo no se guarda ningun dato
                with transaction.atomic():
                    # convierte el string a tipo json
                    vents = json.loads(request.POST['vents'])
                    # crea una instancia y guarda los datos de la factura
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.type = 'sale'
                    sale.save()
                    # itera los productos de la factura y los guarda en el detalle
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id': sale.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Creación de una venta '
        context['entity'] = 'Venta'
        context['entity_pl'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['date_now'] = datetime.now()
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class SaleDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = 'erp.delete_sale'
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('erp:sale_list')
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
        context['title'] = ' Eliminación de una venta '
        context['entity'] = 'Venta'
        context['entity_pl'] = 'Ventas'
        context['list_url'] = reverse_lazy('erp:sale_list')
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class SaleInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('sale/invoice.html')
            context = {
                'title': 'Venta',
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
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
        return HttpResponseRedirect(reverse_lazy('erp:sale_list'))
