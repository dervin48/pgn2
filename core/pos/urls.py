from django.urls import path
from core.pos.views.category.views import *
from core.pos.views.servicio.views import *
from core.pos.views.client.views import *
from core.pos.views.company.views import CompanyUpdateView
from core.pos.views.dashboard.views import *
from core.pos.views.product.views import *
from core.pos.views.sale.views import *
from core.pos.views.into.views import *
from core.pos.views.cargo.views import *

urlpatterns = [
    # dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # category
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # cargo
    path('cargo/', CargoListView.as_view(), name='cargo_list'),
    path('cargo/add/', CargoCreateView.as_view(), name='cargo_create'),
    path('cargo/update/<int:pk>/', CargoUpdateView.as_view(), name='cargo_update'),
    path('cargo/delete/<int:pk>/', CargoDeleteView.as_view(), name='cargo_delete'),
    # servicio
    path('servicio/', ServicioListView.as_view(), name='servicio_list'),
    path('servicio/add/', ServicioCreateView.as_view(), name='servicio_create'),
    path('servicio/update/<int:pk>/', ServicioUpdateView.as_view(), name='servicio_update'),
    path('servicio/delete/<int:pk>/', ServicioDeleteView.as_view(), name='servicio_delete'),
    # client
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # product
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # sale
    path('sale/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    # sale
    path('into/', IntoListView.as_view(), name='into_list'),
    path('into/add/', IntoCreateView.as_view(), name='into_create'),
    path('into/delete/<int:pk>/', IntoDeleteView.as_view(), name='into_delete'),
    path('into/update/<int:pk>/', IntoUpdateView.as_view(), name='into_update'),
    path('into/invoice/pdf/<int:pk>/', IntoInvoicePdfView.as_view(), name='into_invoice_pdf'),
    # company
    path('company/update/', CompanyUpdateView.as_view(), name='company_update'),
]
