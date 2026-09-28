from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views  # <-- Safe authentication view toolkit
from billing.views import checkout_view, process_transaction
from management.views import admin_dashboard, portal_router_view, home_view

urlpatterns = [
    # 1. Base Entry Public Landing Page & Custom Auth Views
    path('', home_view, name='public_home'),
    path('login/', auth_views.LoginView.as_view(template_name='management/login.html'), name='custom_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='public_home'), name='logout'),
    
    # 2. Automated Traffic Role-Router (Handles portal redirection after login)
    path('portal-router/', portal_router_view, name='portal_router'),
    
    # 3. Core Operational Portals
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    path('billing/', checkout_view, name='billing_checkout'),
    path('billing/checkout/process/', process_transaction, name='process_transaction'),
]
