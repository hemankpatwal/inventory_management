from django.shortcuts import render, redirect
from .models import Product, Supplier, SalesOrder, StockMovement
from .forms import ProductForm, SupplierForm, SalesOrderForm, StockMovementForm

#Home Page
def home(request):
    return render(request, 'core/home.html')

# Add Product
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'core/add_product.html', {'form': form})

# List Products
def list_products(request):
    products = Product.objects.all()
    return render(request, 'core/product_list.html', {'products': products})

# Add Supplier
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'core/add_supplier.html', {'form': form})

# List Suppliers
def list_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'core/supplier_list.html', {'suppliers': suppliers})

# Add Stock Movement
def add_stock_movement(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            stock_movement = form.save()
            product = stock_movement.product
            if stock_movement.movement_type == 'in':
                product.stock_quantity += stock_movement.quantity
            else:
                product.stock_quantity -= stock_movement.quantity
            product.save()
            return redirect('product_list')
    else:
        form = StockMovementForm()
    return render(request, 'core/add_stock_movement.html', {'form': form})

# Create Sale Order
def create_sale_order(request):
    if request.method == 'POST':
        form = SalesOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            product = order.product
            if product.stock_quantity >= order.quantity:
                order.total_price = product.price * order.quantity
                order.save()
                product.stock_quantity -= order.quantity
                product.save()
                return redirect('sale_order_list')
            else:
                form.add_error(None, 'Not enough stock')
    else:
        form = SalesOrderForm()
    return render(request, 'core/create_sale_order.html', {'form': form})

# View to list all sale orders
def sale_order_list(request):
    sale_orders = SalesOrder.objects.all()
    return render(request, 'core/sale_order_list.html', {'sale_orders': sale_orders})

# View to check stock levels
def stock_level_check(request):
    products = Product.objects.all()
    return render(request, 'core/stock_level_check.html', {'products': products})