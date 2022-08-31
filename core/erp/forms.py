from datetime import datetime

from betterforms.multiform import MultiModelForm
from django.forms import *

from core.erp.models import Client, Abono, Tecnic, Category, Product, Sale, Zone, Pay, Services, Invoice, JobTecnic


class ClientForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['enable'].widget.attrs['class'] = 'custom-control-input'
        self.fields['enable'].widget.attrs['value'] = 'checked value'
        self.fields['active'].widget.attrs['class'] = 'custom-control-input'
        self.fields['active'].widget.attrs['value'] = 'checked value'

    class Meta:
        model = Client
        fields = '__all__'
        # etiqueta de los campos
        labels = {
            'name': 'Nombre Cliente *',
            'cuit': 'DNI / CUIT *',
            'odorizador': 'Tipo de Abono *',
        }
        # personaliza los campos
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del cliente',
                }
            ),
            'cuit': TextInput(
                attrs={
                    'placeholder': 'Ingrese DNI / CUIT',
                }
            ),
            'odorizador': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
        }
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # metodo que contiene los errores
    # comprueba que tiene menos de 50 caracteres y agrega el error a la variable diccionario cleanned
    def clean(self):
        cleanned = super().clean()
        if len(cleanned['name']) <= 0:
            raise forms.ValidationError('Validación xxx')
            # self.add_error('name', 'Le faltan caracteres')
        print(cleanned)
        return cleanned


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # se utiliza para eliminar la renderizacion dinamica de los componentes de la clase bootstrap
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        # etiqueta de los campos
        labels = {
            'name': 'Nombre Categoria *',
            'desc': 'Descripción',
        }
        # personaliza los campos
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del cliente',
                }
            ),
            'desc': TextInput(
                attrs={
                    'placeholder': 'Ingrese descripción de la categoria',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # metodo que contiene los errores
    # comprueba que si tiene menos de 0 caracteres y agrega el error a la variable diccionario cleanned
    def clean(self):
        cleanned = super().clean()
        if len(cleanned['name']) <= 0:
            raise forms.ValidationError('Validación xxx')
            # self.add_error('name', 'Le faltan caracteres')
        print(cleanned)
        return cleanned


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del producto',
                }
            ),
            'cat': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class AbonoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Abono
        fields = '__all__'
        exclude = ('date_created', 'date_updated')
        # etiqueta de los campos
        labels = {
            'name': 'Nombre Abono',
            'price': 'Precio',
        }
        # personaliza los campos
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del abono',
                }
            ),
            'price': TextInput(
                attrs={
                    'placeholder': 'Ingrese precio del abono',
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # metodo que contiene los errores
    # comprueba que tiene menos de 50 caracteres y agrega el error a la variable diccionario cleanned
    def clean(self):
        cleanned = super().clean()
        if len(cleanned['name']) <= 0:
            raise forms.ValidationError('Validación xxx')
            # self.add_error('name', 'Le faltan caracteres')
        print(cleanned)
        return cleanned


class TecnicForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Tecnic
        fields = '__all__'
        # etiqueta de los campos
        labels = {
            'name': 'Nombre Técnico',
            'desc': 'Descripción',
        }
        # personaliza los campos
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del Técnico',
                }
            ),
            'desc': TextInput(
                attrs={
                    'placeholder': 'Ingrese descripción',
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # metodo que contiene los errores
    # comprueba que tiene menos de 50 caracteres y agrega el error a la variable diccionario cleanned
    def clean(self):
        cleanned = super().clean()
        if len(cleanned['name']) <= 0:
            raise forms.ValidationError('Validación xxx')
            # self.add_error('name', 'Le faltan caracteres')
        print(cleanned)
        return cleanned


class JobTecnicForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = JobTecnic
        fields = ('tecnic', 'zone', 'date')
        # etiqueta de los campos
        # personaliza los campos

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Sale
        fields = '__all__'
        # etiqueta de los campos
        labels = {
            'name': 'Nombre Cliente *',
            'cuit': 'DNI / CUIT *',
            'odorizador': 'Tipo de Abono *',
        }
        # personaliza los campos
        widgets = {
            'cli': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'autofocus': True,
                }),
            'date_joined': DateInput(format='%Y-%m-%d',
                                     attrs={
                                         'class': 'form-control datetimepicker-input',
                                         'value': datetime.now().strftime('%d-%m-%Y'),
                                         'autocomplete': 'off',
                                         'id': 'date_joined',
                                         'data-target': '#date_joined',
                                         'data-toggle': 'datetimepicker',
                                     }),
            'iva': TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'class': 'form-control ',
                'readonly': True,
            }),
            'total': TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
            }),
        }


class InvoiceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Invoice
        fields = '__all__'
        # personaliza los campos
        widgets = {
            'cli': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'autofocus': True,
                }),
        }
        exclude = ['date_joined', 'subtotal', 'iva', 'total', 'type']


class ServicesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        # self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Services
        fields = ['odorizador', 'cant_odo', 'aerosoles', 'cant_aer', 'goteos', 'cant_got']
        # etiqueta de los campos

        # personaliza los campos

    # def save(self, commit=True):
    #     data = {}
    #     form = super()
    #     try:
    #         if form.is_valid():
    #             form.save()
    #         else:
    #             data['error'] = form.errors
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return data

    # metodo que contiene los errores
    # comprueba que tiene menos de 50 caracteres y agrega el error a la variable diccionario cleanned
    # def clean(self):
    #     cleanned = super().clean()
    #     if len(cleanned['cli']) <= 0:
    #         raise forms.ValidationError('Validación xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     print(cleanned)
    #     return cleanned


class ZoneForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['enable'].widget.attrs['class'] = 'custom-control-input'
        self.fields['enable'].widget.attrs['value'] = 'checked value'

    class Meta:
        model = Zone
        fields = '__all__'
        # personaliza los campos
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre de la zona',
                }
            ),
            'desc': TextInput(
                attrs={
                    'placeholder': 'Ingrese una descripción de la zona',
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # metodo que contiene los errores
    # comprueba que tiene menos de 50 caracteres y agrega el error a la variable diccionario cleanned
    def clean(self):
        cleanned = super().clean()
        if len(cleanned['name']) <= 0:
            raise forms.ValidationError('Validación xxx')
            # self.add_error('name', 'Le faltan caracteres')
        print(cleanned)
        return cleanned


class PayForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['required'] = 'required'
            # form.field.widget.attrs['autocomplete'] = 'off'
        # self.fields['cli'].widget.attrs['class'] = 'form-control select2'
        # self.fields['sale'].widget.attrs['class'] = 'form-control select2'
        self.fields['date_pay'].initial = datetime.now()

    class Meta:
        model = Pay
        fields = '__all__'
        # personaliza los campos
        widgets = {
            'date_pay': DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control',
                       'placeholder': 'Seleccione una fecha',
                       'type': 'date',
                       'value': datetime.now()
                       }),
            'mount': TextInput(
                attrs={
                    'placeholder': 'Ingrese monto cobrado',
                }
            ),
            'cli': Select(
                attrs={
                    'style': 'width: 100%',
                    'autofocus': True,
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # metodo que contiene los errores
    # comprueba que tiene menos de 50 caracteres y agrega el error a la variable diccionario cleanned
    # def clean(self):
    #     cleanned = super().clean()
    #     if len(cleanned['name']) <= 0:
    #         raise forms.ValidationError('Validación xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     print(cleanned)
    #     return cleanned


class ServicesClientForm(MultiModelForm):
    form_classes = {
        'client': ClientForm,
        'services': ServicesForm,
    }


class TestForm(Form):
    client = ModelChoiceField(queryset=Client.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    abono = ModelChoiceField(queryset=Abono.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    search = ModelChoiceField(queryset=Client.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
