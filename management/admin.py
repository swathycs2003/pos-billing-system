from django.contrib import admin
from .models import Supplier, Product, Transaction, TransactionItem, ProductReturn

# Customize the main header text of your Admin site
admin.site.site_header = "POS Admin Portal"
admin.site.site_title = "POS Admin Portal"
admin.site.index_title = "System Management Console"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'cost_price', 'selling_price', 'stock_quantity')
    search_fields = ('name', 'sku', 'category')
    list_filter = ('category', 'supplier')
    list_editable = ('selling_price', 'stock_quantity')  # Change prices/stock directly from the grid!

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name',)

class TransactionItemInline(admin.TabularInline):
    model = TransactionItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'unit_price', 'subtotal')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'cashier', 'timestamp', 'total_amount', 'payment_method')
    list_filter = ('payment_method', 'timestamp')
    search_fields = ('invoice_number',)
    inlines = [TransactionItemInline]

@admin.register(ProductReturn)
class ProductReturnAdmin(admin.ModelAdmin):
    list_display = ('product', 'transaction', 'quantity', 'refund_amount', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('transaction__invoice_number', 'product__name')

