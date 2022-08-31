from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.models import Invoice


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_sales_year_month':
                year = request.POST['year']
                # se va a enviar los datos en un array para trabajar con datatables y ajax

                data = {
                    'name': 'Total de Facturación',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': self.get_graph_sales_year_month(year)
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_graph_sales_year_month(self, year):
        # year = datetime.now().year
        # year = int(year)
        data = []
        try:
            for m in range(1, 13):
                total = Invoice.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(
                    r=Sum('total', default=0)).get('r')
                if total is not None:
                    data.append(float(total))
                else:
                    data.append(0.0)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de Administrador'
        context['entity'] = 'Dashboard'
        context['year'] = datetime.now().year
        return context
