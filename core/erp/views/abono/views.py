from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import AbonoForm
from core.erp.models import Abono, Services


class AbonoListView(ListView):
    model = Abono
    template_name = 'abono/list.html'

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
                for i in Abono.objects.all():
                    data.append(i.toJSON())
            elif action == 'view_abono_client_list':
                data = []
                id = request.POST['id']
                for i in Services.objects.filter(Q(odorizador_id=id) | Q(aerosoles_id=id) | Q(goteos_id=id)):
                    if i.cli.enable:
                        equipos = ''
                        if i.cant_odo > 0:
                            equipos += str(i.cant_odo)
                        if i.cant_aer > 0:
                            if equipos == '':
                                equipos = str(i.cant_aer) + 'A'
                            else:
                                equipos += ', ' + str(i.cant_aer) + 'A'
                        if i.cant_got > 0:
                            if equipos == '':
                                equipos = str(i.cant_got) + 'G'
                            else:
                                equipos += ', ' + str(i.cant_got) + 'G'
                        cli = i.toJSON()
                        cli['equipos'] = equipos
                        print(cli)
                        data.append(cli)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Abonos'
        context['create_url'] = reverse_lazy('erp:abono_create')
        context['list_url'] = reverse_lazy('erp:abono_list')
        context['entity'] = 'Abono'
        context['entity_pl'] = 'Abonos'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class AbonoCreateView(CreateView):
    model = Abono
    form_class = AbonoForm
    template_name = 'abono/create.html'
    success_url = reverse_lazy('erp:abono_list')

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
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Crear abono '
        context['entity'] = 'Abono'
        context['entity_pl'] = 'Abonos'
        context['list_url'] = reverse_lazy('erp:abono_list')
        context['action'] = 'add'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class AbonoUpdateView(UpdateView):
    model = Abono
    form_class = AbonoForm
    template_name = 'abono/create.html'
    success_url = reverse_lazy('erp:abono_list')

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
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Edición de un abono '
        context['entity'] = 'Abono'
        context['entity_pl'] = 'Abonos'
        context['list_url'] = reverse_lazy('erp:abono_list')
        context['action'] = 'edit'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class AbonoDeleteView(DeleteView):
    model = Abono
    template_name = 'abono/delete.html'
    success_url = reverse_lazy('erp:abono_list')

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
        context['title'] = ' Eliminación de un abono '
        context['entity'] = 'Abono'
        context['entity_pl'] = 'Abonos'
        context['list_url'] = reverse_lazy('erp:abono_list')
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


