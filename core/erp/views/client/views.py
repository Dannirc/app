import os
from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from weasyprint import HTML, CSS

from config import settings
from core.erp.forms import ClientForm, ServicesClientForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Client, Pay, Services, Invoice, PayInvoice, Tecnic, Zone, EquipRemove, EquipSuspend, \
    ClientPending


def get_client_should(client_id):
    should = 0
    for i in Invoice.objects.filter(cli_id=client_id):
        should += i.total
        # si existen pagos de la fact iterada
        if PayInvoice.objects.filter(invoice_id=i.id):
            # devuelve pagos de una misma fact
            payes = PayInvoice.objects.filter(invoice_id=i.id)
            total_pay = 0
            # sumo los pagos de una misma fact
            for j in payes:
                total_pay += j.total
            should += -total_pay
    return should


def get_client_abono(client_id):
    abono = 0
    cli_services = Services.objects.filter(cli_id=client_id).get()
    if cli_services.odorizador is not None:
        abono += int(cli_services.odorizador.price) * int(cli_services.cant_odo)
    if cli_services.aerosoles is not None:
        abono += int(cli_services.aerosoles.price) * int(cli_services.cant_aer)
    if cli_services.goteos is not None:
        abono += int(cli_services.goteos.price) * int(cli_services.cant_got)

    return abono


def get_client_equipos(client_id):
    equipos = {'odo': 0, 'aer': 0, 'got': 0}
    try:
        cli_services = Services.objects.get(cli_id=client_id)
        equipos['odo'] = cli_services.cant_odo
        equipos['aer'] = cli_services.cant_aer
        equipos['got'] = cli_services.cant_got
    except Services.DoesNotExist:
        pass

    return equipos


def get_client_equipos_str(client_id):
    equipos = get_client_equipos(client_id)
    string = str(equipos.get('odo'))
    if equipos.get('aer') > 0:
        string += ' ' + str(equipos.get('aer')) + 'A'
    if equipos.get('got') > 0:
        string += ' ' + str(equipos.get('got')) + 'G'

    return string


class ClientListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'erp.view_client'
    model = Client
    template_name = 'client/list.html'

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
                cliEnable = request.POST['cliEnable']
                if cliEnable == 'true':
                    for cli in Client.objects.filter(enable=True):
                        # devuelve un diccionario
                        eq = get_client_equipos(cli.id)
                        dict = cli.toJSON()
                        dict['equipos'] = str(eq.get('odo')) + ', ' + str(eq.get('aer')) + ', ' + str(eq.get('got'))
                        data.append(dict)
                else:
                    for cli in Client.objects.all():
                        # devuelve un diccionario
                        eq = get_client_equipos(cli.id)
                        dict = cli.toJSON()
                        dict['equipos'] = str(eq.get('odo')) + ', ' + str(eq.get('aer')) + ', ' + str(eq.get('got'))
                        data.append(dict)
            elif action == 'search_details_modal':
                data = []
                should = 0
                # itero todas las facturas del cliente
                for i in Invoice.objects.filter(cli_id=request.POST['id']):
                    fact = i.toJSON()
                    should += i.total
                    # devuelve pagos de una misma fact
                    payes = PayInvoice.objects.filter(invoice_id=i.id)
                    # si existen pagos de la fact iterada
                    if payes:
                        totalPay = 0
                        date = ''
                        # sumo los pagos de una misma fact
                        for j in payes:
                            totalPay += j.total
                            date = Pay.objects.get(id=j.pay.id).date_pay
                            # date = Pay.objects.filter(id=j.pay.id).get('date_pay')
                        # estado de la fact
                        if i.total == totalPay:
                            fact['status'] = 'Abonado ' + str(date.strftime("%d/%m/%y"))
                        if i.total < totalPay:
                            fact['status'] = 'A favor $' + str(totalPay - i.total) + ' ' + str(date.strftime("%d/%m/%y"))
                        if i.total > totalPay:
                            fact['status'] = 'Debe $' + str(i.total - totalPay) + ' ' + str(date.strftime("%d/%m/%y"))
                        should += -totalPay
                    else:
                        fact['status'] = 'No Abonada'
                    data.append(fact)
                # ordeno datos (ultimo -> primero)
                data = sorted(data, key=lambda invoice: invoice['id'], reverse=True)
                # envio la deuda total en la ultima posicion de la lista
                if len(data) > 0:
                    data.append(str(should))
            elif action == 'service_down':
                cant_odo = int(request.POST['cant_odo'])
                cant_aer = int(request.POST['cant_aer'])
                cant_got = int(request.POST['cant_got'])
                client_services = Services.objects.filter(cli_id=request.POST['id']).get()
                client = Client.objects.filter(id=request.POST['id']).get()

                if 0 <= cant_odo <= client_services.cant_odo and 0 <= cant_aer <= client_services.cant_aer and 0 <= cant_got <= client_services.cant_got:
                    client_services.cant_odo = client_services.cant_odo - cant_odo
                    client_services.cant_aer = client_services.cant_aer - cant_aer
                    client_services.cant_got = client_services.cant_got - cant_got

                    if request.POST['type_down'] == 'retirar':
                        # agrega a lista de retiros
                        # si no existe creo un registro nuevo
                        if not EquipRemove.objects.filter(cli_id=client.id).exists():
                            equip_remove = EquipRemove()
                            equip_remove.cli = client
                            equip_remove.cantOdo = cant_odo
                            equip_remove.cantAer = cant_aer
                            equip_remove.cantGot = cant_got
                        # de lo contrario, edito el existente
                        else:
                            equip_remove = EquipRemove.objects.filter(cli_id=client.id).get()
                            equip_remove.cantOdo += cant_odo
                            equip_remove.cantAer += cant_aer
                            equip_remove.cantGot += cant_got
                        # agregar a historial de cliente
                        # deshabilito cliente si retiro todos los equipos
                        if client_services.cant_odo == 0 and client_services.cant_aer == 0 and client_services.cant_got == 0:
                            client.enable = False
                            client.save()
                            # agregar a historial de cliente
                        equip_remove.save()
                    if request.POST['type_down'] == 'suspender':
                        # agrego a lista de suspendido
                        # si no existe creo un registro nuevo
                        if not EquipSuspend.objects.filter(cli_id=client.id).exists():
                            equip_suspend = EquipSuspend()
                            equip_suspend.cli = client
                            equip_suspend.cantOdo = cant_odo
                            equip_suspend.cantAer = cant_aer
                            equip_suspend.cantGot = cant_got
                        # de lo contrario, edito el existente
                        else:
                            equip_suspend = EquipSuspend.objects.filter(cli_id=client.id).get()
                            equip_suspend.cantOdo += cant_odo
                            equip_suspend.cantAer += cant_aer
                            equip_suspend.cantGot += cant_got
                        # agregar a historial de cliente
                        # suspendo cliente si no tiene servicios activos
                        if client_services.cant_odo == 0 and client_services.cant_aer == 0 and client_services.cant_got == 0:
                            client.active = False
                            client.save()
                            # agregar a historial de cliente
                        equip_suspend.save()
                    client_services.save()
            elif action == 'search_cant_eq_modal':
                data = {}
                client_services = Services.objects.filter(cli_id=request.POST['id']).get()
                data['client'] = client_services.cli.toJSON()
                data['odorizadores'] = client_services.cant_odo
                data['aerosoles'] = client_services.cant_aer
                data['goteos'] = client_services.cant_got
            elif action == 'client_pending':
                client = Client.objects.filter(id=request.POST['id']).get()
                data['client'] = client.toJSON()
            elif action == 'client_pending_confirm':
                cli_id = request.POST['id']
                date = None
                if request.POST["date"] != '':
                    date = datetime.strptime(request.POST["date"], '%Y-%m-%d')
                obs = request.POST['obs']
                clientPending = ClientPending()
                clientPending.cli = Client.objects.filter(id=cli_id).get()
                clientPending.date = datetime.now()
                clientPending.dateToMake = date
                clientPending.observation = obs
                clientPending.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['create_url'] = reverse_lazy('erp:client_create')
        context['list_url'] = reverse_lazy('erp:client_list')
        context['entity'] = 'Cliente'
        context['entity_pl'] = 'Clientes'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class ClientCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'erp.add_client'
    # model = Client
    form_class = ServicesClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('erp:client_list')
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
                form = self.get_form()
                data = form['client'].save()
                client = Client.objects.latest('id')
                services = form['services'].save(commit=False)
                services.cli = client
                services.save()

            elif action == 'search_zone':
                data = []
                for i in Zone.objects.filter(tecnic_id=request.POST['id']):
                    zone = i.toJSON()
                    data.append(zone)

            else:
                data['error'] = 'No ha ingresado a ninguna opcion'

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Crear cliente '
        context['entity'] = 'Cliente'
        context['entity_pl'] = 'Clientes'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ClientUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = 'erp.change_client'
    model = Client
    form_class = ServicesClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('erp:client_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    # se debe modificar para obtener la instancia a editar
    def get_form_kwargs(self):
        kwargs = super(ClientUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'client': self.object,
            'services': Services.objects.filter(cli_id=self.kwargs['pk']).first(),
        })
        return kwargs

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form['client'].save()
                client = Client.objects.filter(id=self.kwargs['pk']).first()
                services = form['services'].save(commit=False)
                services.cli = client
                services.save()

            elif action == 'search_zone':
                data = []
                for i in Zone.objects.filter(tecnic_id=request.POST['id']):
                    zone = i.toJSON()
                    data.append(zone)

            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Edición de un cliente '
        context['entity'] = 'Cliente'
        context['entity_pl'] = 'Clientes'
        context['list_url'] = reverse_lazy('erp:client_list')
        context['action'] = 'edit'
        context['enable'] = self.object.enable
        return context


class ClientDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = 'erp.delete_client'
    model = Client
    template_name = 'client/delete.html'
    success_url = reverse_lazy('erp:client_list')
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
        context['title'] = ' Eliminación de un cliente '
        context['entity'] = 'Cliente'
        context['entity_pl'] = 'Clientes'
        context['list_url'] = reverse_lazy('erp:client_list')
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class ClientSaldoView(FormView):
    form_class = ClientForm
    template_name = 'client/saldos.html'
    success_url = reverse_lazy('erp:client_saldos')

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'consulta_saldo':
                tecnic_id = int(request.POST['tecnic_id'])
                zone_id = int(request.POST['zone_id'])
                type_pay_id = request.POST['type_pay_id']
                # guardo fecha en string
                date_start = request.POST['date_start']
                date_end = request.POST['date_end']
                # convierto fecha datetime.date
                fecha_desde = datetime.strptime(date_start, '%Y-%m-%d').date()
                fecha_hasta = datetime.strptime(date_end, '%Y-%m-%d').date()
                # se va a enviar los datos en un array para trabajar con datatables y ajax
                data = []
                for i in Client.objects.all():
                    should = 0
                    cant = 0
                    # se consulta la deuda
                    for j in Invoice.objects.filter(cli_id=i.id):
                        if fecha_desde <= j.date_joined <= fecha_hasta:
                            should += j.total
                            cant += 1
                            if PayInvoice.objects.filter(invoice_id=j.id):
                                should += -j.total
                                cant -= 1
                    # for j in PayInvoice.objects.filter(cli_id=i.id):
                    #     should += -j.total
                    #     cant -= 1

                    if should:
                        if tecnic_id == 0 or tecnic_id == i.tecnic.id:
                            if zone_id == 0 or zone_id == i.zone_id:
                                if type_pay_id == '0' or type_pay_id == i.type_pay:
                                    dict = i.toJSON()
                                    dict['should'] = str(should)
                                    dict['cant'] = str(cant)
                                    data.append(dict)

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

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Saldos de clientes '
        context['date_now'] = datetime.now()
        context['entity'] = 'Consulta de saldo'
        context['entity_pl'] = 'Consultas de Saldos'
        context['list_url'] = reverse_lazy('erp:client_saldos')
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class ClientSaldoPdf(View):

    def get(self, request, *args, **kwargs):
        try:
            tecnic_id = kwargs['ti']
            # guardo nombre para mostrarlo en context
            if tecnic_id != 0:
                tecnic = Tecnic.objects.filter(id=tecnic_id).get().name
            else:
                tecnic = "Todos"
            zone_id = kwargs['zi']
            # guardo zona para mostrarlo en context
            if zone_id != 0:
                zone = Zone.objects.filter(id=zone_id).get().name
            else:
                zone = "Todas"
            type_pay_id = kwargs['t_pay']
            # guardo tipo de pago para mostrarlo en context
            if type_pay_id == '0':
                typePay = "Todos"
            if type_pay_id == 'Ef':
                typePay = Client.choices_type_pay[0][1]
            if type_pay_id == 'Tr':
                typePay = Client.choices_type_pay[1][1]
            date_start = kwargs['d_start']
            date_end = kwargs['d_end']

            # convierto fecha datetime.date
            fecha_desde = datetime.strptime(date_start, '%Y-%m-%d').date()
            fecha_hasta = datetime.strptime(date_end, '%Y-%m-%d').date()
            # se va a enviar los datos en un array para trabajar con datatables y ajax
            data = []
            total_should = 0
            for i in Client.objects.all():
                should = 0
                cant = 0
                # se consulta la deuda
                for j in Invoice.objects.filter(cli_id=i.id):
                    if fecha_desde <= j.date_joined <= fecha_hasta:
                        should += j.total
                        cant += 1
                        if PayInvoice.objects.filter(invoice_id=j.id):
                            should += -j.total
                            cant -= 1
                # for j in PayInvoice.objects.filter(cli_id=i.id):
                #     should += -j.total
                #     cant -= 1

                if should:
                    if tecnic_id == 0 or tecnic_id == i.tecnic.id:
                        if zone_id == 0 or zone_id == i.zone_id:
                            if type_pay_id == '0' or type_pay_id == i.type_pay:
                                dict = i.toJSON()
                                total_should = total_should + should
                                dict['should'] = str(should)
                                dict['cant'] = str(cant)
                                data.append(dict)

            # ordeno la lista antes de enviar
            data = sorted(data, key=lambda cliente: cliente['name'])

            # pdf
            template = get_template('client/saldos_pdf.html')
            context = {
                'title': 'Listado de Saldos',
                'invoice': '',
                'data': data,
                'tecnic': tecnic,
                'zone': zone,
                'typePay': typePay,
                'dateStart': fecha_desde,
                'dateEnd': fecha_hasta,
                'total_should': total_should,
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
        return HttpResponseRedirect(reverse_lazy('erp:client_list'))
