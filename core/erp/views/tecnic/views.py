from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import TecnicForm
from core.erp.models import Tecnic


class TecnicListView(ListView):
    model = Tecnic
    template_name = 'tecnic/list.html'

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
                for i in Tecnic.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Técnicos'
        context['create_url'] = reverse_lazy('erp:tecnic_create')
        context['list_url'] = reverse_lazy('erp:tecnic_list')
        context['entity'] = 'Técnico'
        context['entity_pl'] = 'Técnicos'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class TecnicCreateView(CreateView):
    model = Tecnic
    form_class = TecnicForm
    template_name = 'tecnic/create.html'
    success_url = reverse_lazy('erp:tecnic_list')

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
        context['title'] = ' Crear Técnico '
        context['entity'] = 'Técnico'
        context['entity_pl'] = 'Técnicos'
        context['list_url'] = reverse_lazy('erp:tecnic_list')
        context['action'] = 'add'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class TecnicUpdateView(UpdateView):
    model = Tecnic
    form_class = TecnicForm
    template_name = 'tecnic/create.html'
    success_url = reverse_lazy('erp:tecnic_list')

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
        context['title'] = ' Edición de un Técnico '
        context['entity'] = 'Técnico'
        context['entity_pl'] = 'Técnicos'
        context['list_url'] = reverse_lazy('erp:tecnic_list')
        context['action'] = 'edit'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class TecnicDeleteView(DeleteView):
    model = Tecnic
    template_name = 'tecnic/delete.html'
    success_url = reverse_lazy('erp:tecnic_list')

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
        context['title'] = ' Eliminación de un Técnico '
        context['entity'] = 'Técnico'
        context['entity_pl'] = 'Técnicos'
        context['list_url'] = reverse_lazy('erp:tecnic_list')
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


