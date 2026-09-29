from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views  
from management.views import admin_dashboard, portal_router_view, home_view
from django.contrib.auth.models import User  # <-- Added: Needed to build user database profiles

# Define a tiny wrapper function that ensures your test profiles exist in the live database
def create_test_accounts():
    try:
        # 1. Build your master administrative profile if missing
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'swathycs')
            print("Successfully initialized 'admin' user profile.")
            
        # 2. Build your staff cashier profile if missing
        if not User.objects.filter(username='cashier1').exists():
            User.objects.create_user('cashier1', 'cashier@example.com', 'StaffPass123')
            print("Successfully initialized 'cashier1' user profile.")
    except Exception as e:
        print(f"Account auto-generation log trace: {e}")

# Run the account creation logic right when Django initializes your paths
create_test_accounts()

urlpatterns = [
    # 1. Base Entry Public Landing Page & Custom Auth Views
    path('', home_view, name='public_home'),
    path('login/', auth_views.LoginView.as_view(template_name='management/login.html'), name='custom_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='public_home'), name='logout'),
    
    # 2. Automated Traffic Role-Router (Handles portal redirection after login)
    path('portal-router/', portal_router_view, name='portal_router'),
    
    # 3. Core Operational Portals (Cleanly grouped via App routing namespaces)
    path('management/', include('management.urls', namespace='management')),
    path('billing/', include('billing.urls', namespace='billing')), # Handles checkout and transaction processing endpoints
    path('admin/', admin.site.urls), # Standard Django backend manager
]
