from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import EquipSuspend


class EquipSuspendListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'erp.view_equipSuspend'
    model = EquipSuspend
    template_name = 'equipSuspend/list.html'

    # Ejemplo de filtro
    # def get_queryset(self):
    #     return Client.objects.filter(odorizador__price=600)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                # se va a enviar los datos en un array para trabajar con datatables y ajax
                data = []
                for i in EquipSuspend.objects.all():
                        dict = i.toJSON()
                        data.append(dict)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Equipos a Suspendidos'
        context['create_url'] = reverse_lazy('erp:client_list')
        context['list_url'] = reverse_lazy('erp:equipSuspend_list')
        context['entity'] = 'Cliente a Suspender'
        context['entity_pl'] = 'Equipos Suspendidos'
        return context