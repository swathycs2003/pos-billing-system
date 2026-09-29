from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from management.models import Product, Transaction, Supplier, ProductReturn

# 1. PUBLIC HOME PAGE VIEW
def home_view(request):
    """Renders your regular home page template for all visitors"""
    return render(request, 'management/home.html')  

# 2. SECURE PORTAL ROUTER
@login_required(login_url='/login/')
def portal_router_view(request):
    """Routes users to their assigned cockpit immediately after logging in"""
    if request.user.is_superuser or request.user.is_staff:
        # FIXED: Added the 'management:' namespace prefix to point to the correct URL name
        return redirect('management:admin_dashboard')
    else:
        # FIXED: Added the 'billing:' namespace prefix to route cashiers safely
        return redirect('billing:billing_checkout')

# 3. ADMIN PORTAL REPORTING DASHBOARD
@login_required(login_url='/login/')
def admin_dashboard(request):
    # Security Gate: Bounces regular cashiers out of management financials
    if not (request.user.is_superuser or request.user.is_staff):
        # FIXED: Added namespace prefix here as well to prevent hidden crash vectors
        return redirect('billing:billing_checkout')

    total_sales_count = Transaction.objects.count()
    total_revenue = Transaction.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00
    total_products = Product.objects.count()
    total_suppliers = Supplier.objects.count()
    total_returns = ProductReturn.objects.count()
    
    # Context Additions: Grabs data panels matching your dashboard requirements list
    recent_transactions = Transaction.objects.order_by('-timestamp')[:5]
    low_stock_products = Product.objects.filter(stock_quantity__lte=10).order_by('stock_quantity')[:5]

    context = {
        'total_sales_count': total_sales_count,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'total_returns': total_returns,
        'recent_transactions': recent_transactions,
        'low_stock_products': low_stock_products,  
    }
    return render(request, 'management/dashboard.html', context)
