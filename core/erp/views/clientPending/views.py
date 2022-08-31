import os
from datetime import date, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView
from weasyprint import HTML, CSS

from config import settings
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import ClientPending, Tecnic, Services
from core.erp.views.client.views import get_client_should, get_client_equipos_str


class ClientPendingListView(ListView):
    model = ClientPending
    template_name = 'clientPending/list.html'

    # Ejemplo de filtro
    # def get_queryset(self):
    #     return Client.objects.filter(odorizador__price=600)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                # se va a enviar los datos en un array para trabajar con datatables y ajax
                data = []
                if request.POST['id'] == '0':
                    for i in ClientPending.objects.filter(dateRealized__isnull=True):
                        data.append(i.toJSON())
                else:
                    for i in ClientPending.objects.filter(cli__tecnic_id=request.POST['id']).filter(dateRealized__isnull=True):
                        data.append(i.toJSON())
            elif action == 'search_tecnic':
                data = []
                for i in Tecnic.objects.all():
                    tecnic = i.toJSON()
                    data.append(tecnic)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes Pendientes'
        # context['create_url'] = reverse_lazy('')
        context['list_url'] = reverse_lazy('erp:clientPending_list')
        context['delete_all_url'] = reverse_lazy('erp:clientPending_delete_all')
        context['entity'] = 'Cliente Pendiente'
        context['entity_pl'] = 'Clientes Pendientes'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class ClientPendingDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = 'erp.delete_clientPending'
    model = ClientPending
    template_name = 'clientPending/delete.html'
    success_url = reverse_lazy('erp:clientPending_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            print(self.object)
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Eliminación de un cliente pendiente'
        context['entity'] = 'Cliente Pendiente'
        context['entity_pl'] = 'Clientes Pendientes'
        context['list_url'] = reverse_lazy('erp:clientPending_list')
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class ClientPendingDeleteAllView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'erp.delete_clientPending'
    model = ClientPending
    template_name = 'clientPending/delete.html'
    success_url = reverse_lazy('erp:clientPending_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            ClientPending.objects.all().delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Eliminación de todos los clientes pendientes'
        context['entity'] = 'Cliente Pendiente'
        context['entity_pl'] = 'Clientes Pendientes'
        context['list_url'] = reverse_lazy('erp:clientPending_list')
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class ClientPendingListPdf(View):

    def get(self, request, *args, **kwargs):
        try:
            tecnic_id = kwargs['ti']
            # se va a enviar los datos en un array para trabajar con datatables y ajax
            data = []
            # guardo nombre para mostrarlo en context
            if tecnic_id != 0:
                tecnic = Tecnic.objects.filter(id=tecnic_id).get().name
                for i in ClientPending.objects.filter(dateRealized__isnull=True).filter(cli__tecnic_id=tecnic_id):
                    i.cli.name = i.cli.name[:30]
                    if i.cli.address != None:
                        # i.cli.address = (i.cli.address + ' '*35)
                        i.cli.address = i.cli.address[:35]
                    dict = i.toJSON()
                    dict['cant_odo'] = get_client_equipos_str(i.cli.id)
                    data.append(dict)
            else:
                tecnic = "Todos"
                for i in ClientPending.objects.filter(dateRealized__isnull=True):
                    i.cli.name = i.cli.name[:30]
                    if i.cli.address != None:
                        # i.cli.address = (i.cli.address + ' '*35)
                        i.cli.address = i.cli.address[:35]
                    dict = i.toJSON()
                    dict['cant_odo'] = get_client_equipos_str(i.cli.id)
                    # funcion get_client_should() de View Client
                    should = get_client_should(i.cli.id)
                    dict['should'] = '{:,}'.format(int(should)).replace(',', '.')
                    data.append(dict)

            # ordeno la lista antes de enviar
            data = sorted(data, key=lambda cliente: cliente['date'])

            # pdf
            template = get_template('clientPending/clientPendingList_pdf.html')
            context = {
                'title': 'Lista de Clientes Pendientes',
                'data': data,
                'tecnic': tecnic,
                # 'comp': {'name': 'SoftGestion',
                #          'cuit': '11-11111111-1',
                #          'address': 'Rosario, Sta Fe, Argentina',
                #          'phone': '341-3112233',
                #          'web': 'softgestion.com'
                #          },
                'date': date.today().strftime("%d/%m/%y"),
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo2.png')
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')

        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:clientPending_list'))
