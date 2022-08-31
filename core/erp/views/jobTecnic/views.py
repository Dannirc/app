from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from core.erp.forms import JobTecnicForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import JobTecnic, Tecnic, Zone, Client, ClientPending
from core.erp.views.zone.views import getCantClientsByZone, getCantEquipByZone, getFactByZone

import locale


class JobTecnicListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'erp.view_jobTecnic'
    model = JobTecnic
    template_name = 'jobTecnic/list.html'

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
                for i in JobTecnic.objects.filter(zone_id__isnull=False):
                    zone = i.toJSON()
                    data.append(zone)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Historial de Zonas Realizadas'
        context['create_url'] = reverse_lazy('erp:jobTecnic_create')
        context['list_url'] = reverse_lazy('erp:jobTecnic_list')
        context['entity'] = 'Registro de Trabajo'
        context['entity_pl'] = 'Registros de Trabajo'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class JobTecnicCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'erp.add_jobTecnic'
    model = JobTecnic
    form_class = JobTecnicForm
    template_name = 'jobTecnic/create.html'
    success_url = reverse_lazy('erp:dashboard')
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
                jobTecnic = JobTecnic()
                date = request.POST['date']
                tecnicId = request.POST['select_tecnic']
                zoneId = request.POST['select_zone']
                # guardo el trabajo realizado del tecnico
                jobTecnic.date = datetime.strptime(date, '%Y-%m-%d')
                jobTecnic.tecnic = Tecnic.objects.filter(id=tecnicId).get()
                if zoneId != '0':
                    jobTecnic.zone = Zone.objects.filter(id=zoneId).get()
                    jobTecnic.cantClient = getCantClientsByZone(self, zoneId)
                    jobTecnic.cantEquipos = getCantEquipByZone(self, zoneId)['cant_odo']
                    jobTecnic.totalFact = getFactByZone(self, zoneId)
                jobTecnic.save()
                # clientes pendientes
                # recibo los id y los convierto a una lista
                lista = request.POST['datosTabla']
                lista = lista.split(',')
                if not lista == ['']:
                    # por cada iteracion genero un nuevo cliente pendiente
                    for i in lista:
                        clientPending = ClientPending()
                        clientPending.cli = Client.objects.filter(id=i).get()
                        clientPending.date = jobTecnic.date
                        # obtengo los datos del request.POST
                        # enviados a traves de los td name (ID-Fecha, ID-Motivo) de la tabla
                        if not request.POST[i + "-Fecha"] == '':
                            clientPending.dateToMake = datetime.strptime(request.POST[i + "-Fecha"], '%Y-%m-%d')
                        clientPending.observation = request.POST[i + "-Motivo"]
                        clientPending.save()

                # clientes pendientes realizados
                cliRealizedList = request.POST['clientRealizedList']
                cliRealizedList = cliRealizedList.split(',')
                if not cliRealizedList == ['']:
                    # por cada iteracion genero un nuevo cliente pendiente
                    for i in cliRealizedList:
                        clientPending = ClientPending()
                        clientPending = ClientPending.objects.filter(id=i).get()
                        clientPending.dateRealized = jobTecnic.date
                        clientPending.save()
            elif action == 'search_tecnic':
                data = []
                for i in Tecnic.objects.all():
                    tecnic = i.toJSON()
                    data.append(tecnic)
            elif action == 'search_zone':
                data = []
                for i in Zone.objects.filter(tecnic_id=request.POST['id']):
                    zone = i.toJSON()
                    data.append(zone)
            elif action == 'search_client':
                data = []
                for i in Client.objects.filter(zone_id=request.POST['id'], enable=True, active=True):
                    client = [i.id, i.name]
                    data.append(client)
                data = sorted(data, key=lambda cliente: cliente[1])
            elif action == 'search_client_pending':
                data = []
                for i in ClientPending.objects.filter(cli__tecnic_id=request.POST['id']).filter(
                        dateRealized__isnull=True):
                    client = [i.id, i.cli.name]
                    data.append(client)
                data = sorted(data, key=lambda cliente: cliente[1])
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Cargar un nuevo registro de trabajo '
        context['entity'] = 'Trabajo'
        context['entity_pl'] = 'Trabajos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class JobTecnicUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = 'erp.change_jobTecnic'
    model = JobTecnic
    form_class = JobTecnicForm
    template_name = 'zone/create.html'
    success_url = reverse_lazy('erp:jobTecnic_list')
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
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Edición de una planilla de trabajo '
        context['entity'] = 'Planilla de Trabajo'
        context['entity_pl'] = 'Planillas de Trabajo'
        context['list_url'] = reverse_lazy('erp:jobTecnic_list')
        context['action'] = 'edit'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class JobTecnicDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = 'erp.delete_jobTecnic'
    model = JobTecnic
    template_name = 'jobTecnic/delete.html'
    success_url = reverse_lazy('erp:jobTecnic_list')
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
        context['title'] = ' Eliminación de una planilla de trabajo '
        context['entity'] = 'Planilla de Trabajo'
        context['entity_pl'] = 'Planillas de Trabajo'
        context['list_url'] = reverse_lazy('erp:jobTecnic_list')
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class JobTecnicMonthlyPlanning(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'erp.view_jobTecnic'
    model = JobTecnic
    template_name = 'jobTecnic/month_planning.html'

    # Ejemplo de filtro
    # def get_queryset(self):
    #     return Client.objects.filter(odorizador__price=600)

    def get_dateValid(self, date):
        while True:
            if date.weekday() <= 4:
                break
            date = date + timedelta(days=1)
        return date

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
                locale.setlocale(locale.LC_TIME, "es_AR.utf8")
                # values_list devuelve tuplas de los objetos
                # si solo solicitamos un campos (ej: id) le podemos pasar (flat=True) devolvera solo los valores
                # zone_list = list(Zone.objects.filter(enable=True).values_list('id', flat=True))
                zone_list = Zone.objects.filter(enable=True)
                zone_last_register = []
                for zone in zone_list:
                    if JobTecnic.objects.filter(zone_id=zone.id).exists():
                        zone_last_register.append(JobTecnic.objects.filter(zone_id=zone.id).latest('date'))
                zone_last_register.sort(key=lambda jobTecnic: jobTecnic.date)
                # iterar la fecha para cada tecnico diferente
                list_date_tecnic = {}
                for register in zone_last_register:
                    tecnic = register.zone.tecnic.name
                    if list_date_tecnic.get(tecnic) is None:
                        list_date_tecnic[tecnic] = datetime.now()
                    date_of_work = self.get_dateValid(list_date_tecnic[tecnic])
                    next_date = date_of_work
                    zone = register.zone.toJSON()
                    zone['date'] = register.date
                    zone['date_of_work'] = ''
                    if register.date.month != datetime.now().month:
                        if JobTecnic.objects.filter(tecnic_id=register.tecnic.id, date=date_of_work):
                            date_of_work = date_of_work + timedelta(days=1)
                            zone['date_of_work'] = self.get_dateValid(date_of_work).strftime('%A %d')
                            next_date = self.get_dateValid(date_of_work + timedelta(days=1))
                        else:
                            zone['date_of_work'] = self.get_dateValid(date_of_work).strftime('%A %d')
                            next_date = self.get_dateValid(date_of_work + timedelta(days=1))
                    else:
                        if JobTecnic.objects.filter(zone_id=register.zone.id, date__month=datetime.now().month).count() <= 1:
                            if JobTecnic.objects.filter(tecnic_id=register.tecnic.id, date=date_of_work):
                                date_of_work = date_of_work + timedelta(days=1)
                                zone['date_of_work'] = self.get_dateValid(date_of_work).strftime('%A %d')
                                next_date = self.get_dateValid(date_of_work + timedelta(days=1))
                            else:
                                zone['date_of_work'] = self.get_dateValid(date_of_work).strftime('%A %d')
                                next_date = self.get_dateValid(date_of_work + timedelta(days=1))
                        else:
                            zone['date_of_work'] = 'Servicio Completo'
                    list_date_tecnic[tecnic] = next_date
                    data.append(zone)

                # for zone in zone_list:
                #     register = JobTecnic.objects.filter(zone_id=zone.id, zone_id__isnull=False).last()
                #     zone = zone.toJSON()
                #     zone['date'] = ''
                #     zone['nextDate'] = ''
                #     if register is not None:
                #         zone['date'] = register.date
                #         if register.date.month == datetime.now().month:
                #             date = register.date + timedelta(days=15)
                #             # zone['nextDate'] = date.strftime('%d/%m/%Y')
                #             zone['nextDate'] = date.strftime('%A %d')
                #             print(zone['nextDate'])
                #     data.append(zone)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Planificacion de Zonas'
        context['create_url'] = reverse_lazy('erp:jobTecnicMonthPlanning_list')
        context['list_url'] = reverse_lazy('erp:jobTecnicMonthPlanning_list')
        context['entity'] = 'Planificación de Zona'
        context['entity_pl'] = 'Planificación de Zonas'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context