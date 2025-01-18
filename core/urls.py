from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.list_products, name='product_list'),
    path('product/add/', views.add_product, name='add_product'),
    path('suppliers/', views.list_suppliers, name='supplier_list'),
    path('supplier/add/', views.add_supplier, name='add_supplier'),
    path('stock_movement/add/', views.add_stock_movement, name='add_stock_movement'),
    path('sale_order/create/', views.create_sale_order, name='create_sale_order'),
]