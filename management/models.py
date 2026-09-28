from django.db import models
from django.contrib.auth.models import User

# 1. SUPPLIER MANAGEMENT
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# 2. PRODUCT CRUD
class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)  # Barcode / Item ID
    category = models.CharField(max_length=100, default="Textiles")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='products')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.sku}) - Qty: {self.stock_quantity}"

# 3. BILLING / TRANSACTION MANAGEMENT
class Transaction(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('UPI', 'UPI/Online'),
    ]
    invoice_number = models.CharField(max_length=100, unique=True)
    cashier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Tracks which staff made the sale
    timestamp = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='CASH')

    def __str__(self):
        return f"Invoice {self.invoice_number} - Total: {self.total_amount}"

# 4. TRANSACTION ITEMS
class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)  # Protect prevents deleting products tied to history
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

# 5. PRODUCT RETURN HANDLING
class ProductReturn(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    reason = models.TextField()
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return: {self.product.name} from Invoice {self.transaction.invoice_number}"


    
