from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from management.models import Product, Transaction, Supplier, ProductReturn
from django.db.models import Sum

# 1. PUBLIC HOME PAGE VIEW
def home_view(request):
    """Renders your regular home page template for all visitors"""
    return render(request, 'management/home.html')  # Make sure this matches your filename!

# 2. SECURE PORTAL ROUTER
@login_required(login_url='/login/')
def portal_router_view(request):
    """Routes users to their assigned cockpit immediately after logging in"""
    if request.user.is_superuser or request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('billing_checkout')

# 3. ADMIN PORTAL REPORTING DASHBOARD
@login_required(login_url='/login/')
def admin_dashboard(request):
    # Security Gate: Bounces regular cashiers out of management financials
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('billing_checkout')

    total_sales_count = Transaction.objects.count()
    total_revenue = Transaction.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00
    total_products = Product.objects.count()
    total_suppliers = Supplier.objects.count()
    total_returns = ProductReturn.objects.count()
    recent_transactions = Transaction.objects.order_by('-timestamp')[:5]

    context = {
        'total_sales_count': total_sales_count,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'total_returns': total_returns,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'management/dashboard.html', context)
