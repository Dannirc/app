import datetime
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from weasyprint import HTML, CSS

from config import settings
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import EquipRemove


class EquipRemoveListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'erp.view_equipRemove'
    model = EquipRemove
    template_name = 'equipRemove/list.html'

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
                for i in EquipRemove.objects.all():
                    dict = i.toJSON()
                    data.append(dict)
            elif action == 'service_down':
                cant_odo = int(request.POST['cant_odo'])
                cant_aer = int(request.POST['cant_aer'])
                cant_got = int(request.POST['cant_got'])
                id = request.POST['id']
                equip_remove = EquipRemove.objects.get(cli_id=id)
                if cant_odo == equip_remove.cantOdo and cant_aer == equip_remove.cantAer and cant_got == equip_remove.cantGot:
                    equip_remove.delete()
                elif 0 <= cant_odo <= equip_remove.cantOdo and 0 <= cant_aer <= equip_remove.cantAer and 0 <= cant_got <= equip_remove.cantGot:
                    equip_remove.cantOdo -= cant_odo
                    equip_remove.cantAer -= cant_aer
                    equip_remove.cantGot -= cant_got
                    equip_remove.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Equipos a Retirar'
        context['create_url'] = reverse_lazy('erp:client_list')
        context['list_url'] = reverse_lazy('erp:equipRemove_list')
        context['entity'] = 'Cliente a Retirar'
        context['entity_pl'] = 'Equipos Retirados'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class EquipRemovePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('equipRemove/details_print.html')
            context = {
                'title': 'Retiro de Equipos',
                'equipRemove': EquipRemove.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'SoftGestion',
                         'cuit': '11-11111111-1',
                         'address': 'Rosario, Sta Fe, Argentina',
                         'phone': '341-3112233',
                         'web': 'softgestion.com'
                         },
                'date': datetime.date.today(),
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo2.png')
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:equipRemove_list'))
