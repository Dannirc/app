from django.urls import reverse_lazy
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('erp:dashboard')
        context['client_url'] = reverse_lazy('erp:client_list')
        return context