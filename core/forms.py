from django import forms
from .models import Product, Supplier, SalesOrder, StockMovement
from django.core.exceptions import ValidationError
from decimal import Decimal

# Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock_quantity', 'supplier']

    # Custom validation for price and stock_quantity
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= Decimal(0):
            raise ValidationError("Price must be greater than zero.")
        return price

    def clean_stock_quantity(self):
        stock_quantity = self.cleaned_data.get('stock_quantity')
        if stock_quantity < 0:
            raise ValidationError("Stock quantity cannot be negative.")
        return stock_quantity

# Supplier Form
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'address']

    # Custom validation for phone number (must be 10 digits)
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 10 or not phone.isdigit():
            raise ValidationError("Phone number must be 10 digits.")
        return phone

# Sales Order Form
class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ['product', 'quantity', 'status']

    # Custom validation for quantity (must be positive and not exceed stock)
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        if quantity > product.stock_quantity:
            raise ValidationError(f"Not enough stock for {product.name}.")
        return quantity

    # Calculate total price based on quantity and product price
    def save(self, commit=True):
        instance = super().save(commit=False)
        product = instance.product
        instance.total_price = product.price * instance.quantity
        if commit:
            instance.save()
        return instance

# Stock Movement Form
class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'quantity', 'movement_type', 'notes']

    # Custom validation for quantity (cannot be negative in movement)
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        movement_type = self.cleaned_data.get('movement_type')
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        return quantity

    # Ensure the stock quantity update is valid
    def save(self, commit=True):
        instance = super().save(commit=False)
        product = instance.product
        movement_type = instance.movement_type

        if movement_type == 'in':
            product.stock_quantity += instance.quantity
        elif movement_type == 'out':
            if product.stock_quantity >= instance.quantity:
                product.stock_quantity -= instance.quantity
            else:
                raise ValidationError(f"Not enough stock for {product.name}.")
        
        if commit:
            instance.save()
            product.save()
        return instance
