from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from core.erp.forms import ClientForm, CategoryForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Category


class CategoryListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'erp.view_category'
    model = Category
    template_name = 'category/list.html'

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
                for i in Category.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # safe=False se utiliza cuando se quiere serializar objetos que no son del diccionario
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Categorias'
        context['create_url'] = reverse_lazy('erp:category_create')
        context['list_url'] = reverse_lazy('erp:category_list')
        context['entity'] = 'Categoria'
        context['entity_pl'] = 'Categorias'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class CategoryCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'erp.add_category'
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('erp:category_list')
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
        context['title'] = ' Crear categoria '
        context['entity'] = 'Categoria'
        context['entity_pl'] = 'Categorias'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class CategoryUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = 'erp.change_client'
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('erp:category_list')
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
        context['title'] = ' Edición de una categoria '
        context['entity'] = 'Categoria'
        context['entity_pl'] = 'Categorias'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'edit'
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class CategoryDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = 'erp.delete_client'
    model = Category
    template_name = 'category/delete.html'
    success_url = reverse_lazy('erp:category_list')
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
        context['title'] = ' Eliminación de una categoria '
        context['entity'] = 'Categoria'
        context['entity_pl'] = 'Categorias'
        context['list_url'] = reverse_lazy('erp:category_list')
        # Ejemplo de modificar el modelo a enviar
        # context['object_list'] = Sale.objects.all()
        return context


class ClientFormView(FormView):
    form_class = ClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('erp:client_list')