import json
import os
from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from weasyprint import HTML, CSS

from config import settings
from core.erp.forms import ZoneForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Zone, Client, Services

# functions


def getCantClientsByZone(self, zone_id):
    clients = Client.objects.filter(zone_id=zone_id, enable=True)
    return clients.count()


def getCantEquipByZone(self, zone_id):
    clients = Client.objects.filter(zone_id=zone_id, enable=True)
    cant_odo = 0
    cant_aer = 0
    cant_got = 0
    data = {}
    for cli in clients:
        services_cli = Services.objects.filter(cli_id=cli.id).first()
        if services_cli.cant_odo >= 0:
            cant_odo += int(services_cli.cant_odo)
        if services_cli.cant_aer >= 0:
            cant_aer += int(services_cli.cant_aer)
        if services_cli.cant_got >= 0:
            cant_got += int(services_cli.cant_got)
    data['cant_odo'] = cant_odo
    data['cant_aer'] = cant_aer
    data['cant_got'] = cant_got
    return data


def getFactByZone(self, zone_id):
    total_fact = 0
    for cli in Client.objects.filter(zone_id=zone_id, enable=True):
        services_cli = Services.objects.filter(cli_id=cli.id).first()
        if services_cli.odorizador is not None:
            total_fact += int(services_cli.odorizador.price) * int(services_cli.cant_odo)
        if services_cli.aerosoles is not None:
            total_fact += int(services_cli.aerosoles.price) * int(services_cli.cant_aer)
        if services_cli.goteos is not None:
            total_fact += int(services_cli.goteos.price) * int(services_cli.cant_got)
    return total_fact


def getAbonoByClient(self, client_id):
    abono = 0
    services_cli = Services.objects.filter(cli_id=client_id).get()
    if services_cli.odorizador is not None:
        abono = int(services_cli.odorizador.price) * int(services_cli.cant_odo)
    if services_cli.aerosoles is not None:
        abono += int(services_cli.aerosoles.price) * int(services_cli.cant_aer)
    if services_cli.goteos is not None:
        abono += int(services_cli.goteos.price) * int(services_cli.cant_got)
    return abono


def getCantEquipByClient(self, client_id):
    data = {}
    services_cli = Services.objects.filter(cli_id=client_id).first()
    if services_cli.cant_odo >= 0:
        data['cant_odo'] = int(services_cli.cant_odo)
    if services_cli.cant_aer >= 0:
        data['cant_aer'] = int(services_cli.cant_aer)
    if services_cli.cant_got >= 0:
        data['cant_got'] = int(services_cli.cant_got)
    return data


class ZoneListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'erp.view_zone'
    model = Zone
    template_name = 'zone/list.html'

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
                for i in Zone.objects.all():
                    data.append(i.toJSON())
            elif action == 'view_zone_list':
                data = []
                for i in Client.objects.filter(zone_id=request.POST['id']):
                    if i.enable:
                        abono = 0
                        cant_odo = 0
                        for j in Services.objects.filter(cli_id=i.id):
                            # se calcula el abono total del cliente
                            if j.odorizador is not None:
                                abono = int(j.odorizador.price) * int(j.cant_odo)
                            if j.aerosoles is not None:
                                abono += int(j.aerosoles.price) * int(j.cant_aer)
                            if j.goteos is not None:
                                abono += int(j.goteos.price) * int(j.cant_got)
                            # asigna cantidad de equipos
                            cant_odo = int(j.cant_odo)

                        dict = i.toJSON()
                        dict['abono'] = str(abono)
                        dict['cant_odo'] = str(cant_odo)
                        data.append(dict)

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Zonas'
        context['create_url'] = reverse_lazy('erp:zone_create')
        context['list_url'] = reverse_lazy('erp:zone_list')
        context['entity'] = 'Zona'
        context['entity_pl'] = 'Zonas'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class ZoneCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'erp.add_zone'
    model = Zone
    form_class = ZoneForm
    template_name = 'zone/create.html'
    success_url = reverse_lazy('erp:zone_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Crear zona '
        context['entity'] = 'Zona'
        context['entity_pl'] = 'Zonas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class ZoneUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = 'erp.change_zone'
    model = Zone
    form_class = ZoneForm
    template_name = 'zone/create.html'
    success_url = reverse_lazy('erp:zone_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                id = int(kwargs['pk'])
                tecnic_id = int(request.POST['tecnic'])
                zone = Zone.objects.get(id=id)
                # si el tecnico fue cambiado
                # asigna a los clientes el nuevo tecnico
                print(type(zone.tecnic_id), type(tecnic_id))
                if zone.tecnic_id != tecnic_id:
                    clients = Client.objects.filter(zone_id=id)
                    print(clients)
                    for client in clients:
                        client.tecnic_id = tecnic_id
                        client.save()
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Edición de una zona '
        context['entity'] = 'Zona'
        context['entity_pl'] = 'Zonas'
        context['list_url'] = reverse_lazy('erp:zone_list')
        context['action'] = 'edit'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class ZoneDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = 'erp.delete_zone'
    model = Zone
    template_name = 'zone/delete.html'
    success_url = reverse_lazy('erp:zone_list')
    url_redirect = success_url

    @method_decorator(login_required)
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
        context['title'] = ' Eliminación de una zona '
        context['entity'] = 'Zona'
        context['entity_pl'] = 'Zonas'
        context['list_url'] = reverse_lazy('erp:zone_list')
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class ZoneRoutePdfView(View):

    def get(self, request, *args, **kwargs):
        data = []
        try:
            template = get_template('zone/route.html')
            zone_id = self.kwargs['pk']
            for i in Client.objects.filter(zone_id=zone_id, enable=True):
                i.name = i.name[0:35]
                if i.address != None:
                    i.address = i.address[0:35]
                dict = i.toJSON()
                dict['abono'] = str(getAbonoByClient(self, i.id))
                dict['cant_odo'] = str(getCantEquipByClient(self, i.id)['cant_odo'])
                # mostrar en el template pdf
                # dict['cant_aer'] = str(getCantEquipByClient(self, i.id)['cant_aer'])
                # dict['cant_got'] = str(getCantEquipByClient(self, i.id)['cant_got'])
                data.append(dict)

            total_cli = getCantClientsByZone(self, zone_id)
            total_eq = getCantEquipByZone(self, zone_id)
            total_fact = getFactByZone(self, zone_id)

            # ordenamos la tabla por posicion del cliente en la planilla
            sorted_data = sorted(data, key=lambda x: x['position'])

            context = {
                'title': 'Planilla de clientes ',
                'zone': Zone.objects.get(pk=self.kwargs['pk']),
                'data': sorted_data,
                'total_clientes': total_cli,
                'total_equipos': total_eq,
                'total_facturado': total_fact,
                'comp': {'name': 'SoftGestion',
                         'cuit': '11-11111111-1',
                         'address': 'Rosario, Sta Fe, Argentina',
                         'phone': '341-3112233',
                         'web': 'softgestion.com'
                         },
                'date': date.today().strftime("%d/%m/%y"),
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo2.png')
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:zone_list'))


class ZoneOrderView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'erp.view_zone'
    model = Zone
    template_name = 'zone/orderZone.html'

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
                data = []
                for i in Client.objects.filter(zone_id=self.kwargs['pk']):
                    if i.enable:
                        abono = 0
                        cant_odo = 0
                        for j in Services.objects.filter(cli_id=i.id):
                            if j.odorizador is not None:
                                abono = int(j.odorizador.price) * int(j.cant_odo)
                            if j.aerosoles is not None:
                                abono += int(j.aerosoles.price) * int(j.cant_aer)
                            if j.goteos is not None:
                                abono += int(j.goteos.price) * int(j.cant_got)
                            # asigna cantidad de equipos
                            cant_odo = int(j.cant_odo)

                        dict = i.toJSON()
                        dict['abono'] = str(abono)
                        dict['cant_odo'] = str(cant_odo)
                        data.append(dict)
                        print(data)
            elif action == 'confirmOrder':
                data = request.POST['data']
                # convierto data string a json
                data = json.loads(data)
                position = 0
                # asigno la posicion del cliente en la zona
                for cli in data:
                    position += 1
                    client = Client.objects.get(id=cli['id'])
                    client.position = position
                    client.save()
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ordenar Zona'
        context['create_url'] = reverse_lazy('erp:zone_create')
        context['list_url'] = reverse_lazy('erp:zone_list')
        context['entity'] = 'Zona'
        context['entity_pl'] = 'Zonas'
        return context
