from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.models import Sale
from core.reports.forms import ReportForm


class ReportSaleView(TemplateView):
    template_name = 'sale/report.html'

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                # se va a enviar los datos en un array para trabajar con datatables y ajax
                data = []
                # el metodo .get si no encuentra el valor, devuelve un valor por defecto
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = Sale.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                for s in search:
                    data.append([
                        s.id,
                        s.cli.name,
                        s.date_joined.strftime('%Y-%m-%d'),
                        format(s.subtotal, '.2f'),
                        format(s.iva, '.2f'),
                        format(s.total, '.2f'),
                    ])

                if search:
                    subtotal = search.aggregate(r=Sum('subtotal', default=0.0)).get('r')
                    iva = search.aggregate(r=Sum('iva', default=0.0)).get('r')
                    total = search.aggregate(r=Sum('total', default=0.0)).get('r')

                    data.append([
                        '---',
                        '---',
                        '---',
                        format(subtotal, '.2f'),
                        format(iva, '.2f'),
                        format(total, '.2f'),
                    ])

            else:
                data['error'] = 'Ha ocurrido un error'

        except Exception as e:
            data['error'] = str(e)
            # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de las Ventas'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('sale_report')
        context['form'] = ReportForm()

        return context
