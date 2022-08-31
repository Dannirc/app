from django.urls import path

from core.erp.views.abono.views import AbonoListView, AbonoCreateView, AbonoUpdateView, AbonoDeleteView
from core.erp.views.category.views import CategoryCreateView, CategoryListView, CategoryUpdateView, CategoryDeleteView
from core.erp.views.clientPending.views import ClientPendingListView, ClientPendingDeleteView, ClientPendingListPdf, \
    ClientPendingDeleteAllView
from core.erp.views.dashboard.views import DashboardView
from core.erp.views.equipRemove.views import EquipRemoveListView, EquipRemovePdfView
from core.erp.views.equipSuspend.views import EquipSuspendListView
from core.erp.views.invoice.views import InvoiceListView, InvoiceCreateView, InvoiceDeleteView, InvoicePdfView
from core.erp.views.jobTecnic.views import JobTecnicCreateView, JobTecnicListView, JobTecnicUpdateView, \
    JobTecnicDeleteView, JobTecnicMonthlyPlanning
from core.erp.views.pay.views import PayListView, PayCreateView, PayUpdateView, PayDeleteView, PayPrintPdfView, \
    PayCreateViewTest
from core.erp.views.product.views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView
from core.erp.views.client.views import *
from core.erp.views.sale.views import SaleCreateView, SaleListView, SaleDeleteView, SaleInvoicePdfView
from core.erp.views.tecnic.views import TecnicListView, TecnicCreateView, TecnicUpdateView, TecnicDeleteView
from core.erp.views.tests.views import TestView
from core.erp.views.zone.views import ZoneListView, ZoneCreateView, ZoneDeleteView, ZoneUpdateView, ZoneRoutePdfView, \
    ZoneOrderView

app_name = 'erp'

urlpatterns = [
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # client
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('client/saldos/', ClientSaldoView.as_view(), name='client_saldos'),
    path('client/saldos/pdf/<int:ti>/<int:zi>/<str:t_pay>/<str:d_start>/<str:d_end>/', ClientSaldoPdf.as_view(),
         name='client_saldos_pdf'),
    # abono
    path('abono/list/', AbonoListView.as_view(), name='abono_list'),
    path('abono/add/', AbonoCreateView.as_view(), name='abono_create'),
    path('abono/update/<int:pk>/', AbonoUpdateView.as_view(), name='abono_update'),
    path('abono/delete/<int:pk>/', AbonoDeleteView.as_view(), name='abono_delete'),
    # tecnic
    path('tecnic/list/', TecnicListView.as_view(), name='tecnic_list'),
    path('tecnic/add/', TecnicCreateView.as_view(), name='tecnic_create'),
    path('tecnic/update/<int:pk>/', TecnicUpdateView.as_view(), name='tecnic_update'),
    path('tecnic/delete/<int:pk>/', TecnicDeleteView.as_view(), name='tecnic_delete'),
    # category
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # product
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # sale
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    # zone
    path('zone/list/', ZoneListView.as_view(), name='zone_list'),
    path('zone/add/', ZoneCreateView.as_view(), name='zone_create'),
    path('zone/update/<int:pk>/', ZoneUpdateView.as_view(), name='zone_update'),
    path('zone/delete/<int:pk>/', ZoneDeleteView.as_view(), name='zone_delete'),
    path('zone/route/pdf/<int:pk>/', ZoneRoutePdfView.as_view(), name='zone_route'),
    path('zone/orderzone/<int:pk>/', ZoneOrderView.as_view(), name='zone_order'),
    # pay
    path('pay/list/', PayListView.as_view(), name='pay_list'),
    path('pay/add/', PayCreateView.as_view(), name='pay_create'),
    path('pay/add/test/', PayCreateViewTest.as_view(), name='pay_create_test'),
    path('pay/update/<int:pk>/', PayUpdateView.as_view(), name='pay_update'),
    path('pay/delete/<int:pk>/', PayDeleteView.as_view(), name='pay_delete'),
    path('pay/print/pdf/<int:pk>/', PayPrintPdfView.as_view(), name='sale_invoice_pdf'),
    # invoice
    path('invoice/list/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoice/add/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoice/delete/<int:pk>/', InvoiceDeleteView.as_view(), name='invoice_delete'),
    path('invoice/pdf/<int:pk>/', InvoicePdfView.as_view(), name='invoice_pdf'),
    # jobTecnic
    path('jobTecnic/list/', JobTecnicListView.as_view(), name='jobTecnic_list'),
    path('jobTecnic/add/', JobTecnicCreateView.as_view(), name='jobTecnic_create'),
    path('jobTecnic/update/<int:pk>/', JobTecnicUpdateView.as_view(), name='jobTecnic_update'),
    path('jobTecnic/delete/<int:pk>/', JobTecnicDeleteView.as_view(), name='jobTecnic_delete'),
    path('jobTecnic/month-planning/', JobTecnicMonthlyPlanning.as_view(), name='jobTecnicMonthPlanning_list'),
    # clientPending
    path('clientPending/list/', ClientPendingListView.as_view(), name='clientPending_list'),
    path('clientPending/delete/<int:pk>/', ClientPendingDeleteView.as_view(), name='clientPending_delete'),
    path('clientPending/delete/all/', ClientPendingDeleteAllView.as_view(), name='clientPending_delete_all'),
    path('clientPending/list/pdf/<int:ti>/', ClientPendingListPdf.as_view(), name='clientPending_list_pdf'),
    # equipRemove
    path('equipRemove/list/', EquipRemoveListView.as_view(), name='equipRemove_list'),
    path('equipRemove/pdf/<int:pk>/', EquipRemovePdfView.as_view(), name='equipRemove_pdf'),
    # equipSuspend
    path('equipSuspend/list/', EquipSuspendListView.as_view(), name='equipSuspend_list'),
    # test
    path('test/', TestView.as_view(), name='test_view'),
]
