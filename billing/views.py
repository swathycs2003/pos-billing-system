import json
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Corrected import path from management.models to billing.models
from management.models import Product, Transaction, TransactionItem

def checkout_view(request):
    # Renders the initial frontend POS dashboard layout
    products = Product.objects.filter(stock_quantity__gt=0)
    return render(request, 'billing/checkout.html', {'products': products})

@csrf_exempt
def process_transaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart = data.get('cart', [])
            payment_method = data.get('payment_method', 'CASH')
            
            if not cart:
                return JsonResponse({'success': False, 'error': 'Cart is empty'}, status=400)
                
            total_amount = 0
            items_to_create = []
            products_to_update = []
            
            # Step 1: Validate stock and calculate total values safely
            for item in cart:
                product_id = item.get('id')
                quantity = int(item.get('quantity', 1))
                
                product = Product.objects.get(id=product_id)
                if product.stock_quantity < quantity:
                    return JsonResponse({'success': False, 'error': f'Insufficient stock for {product.name}'}, status=400)
                
                subtotal = product.selling_price * quantity
                total_amount += subtotal
                
                items_to_create.append({
                    'product': product,
                    'quantity': quantity,
                    'unit_price': product.selling_price,
                    'subtotal': subtotal
                })
                
                # Update inventory counts locally
                product.stock_quantity -= quantity
                products_to_update.append(product)
                
            # Step 2: Save everything inside the database engine securely
            invoice = f"INV-{uuid.uuid4().hex[:8].upper()}"
            transaction = Transaction.objects.create(
                invoice_number=invoice,
                cashier=request.user if request.user.is_authenticated else None,
                total_amount=total_amount,
                payment_method=payment_method
            )
            
            for item in items_to_create:
                TransactionItem.objects.create(
                    transaction=transaction,
                    product=item['product'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    subtotal=item['subtotal']
                )
                
            # Bulk save product stock updates all at once
            for p in products_to_update:
                p.save()
                
            return JsonResponse({
                'success': True, 
                'invoice': invoice,
                'total': float(total_amount)
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
