from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    # Route for the main cashier terminal interface
    path('checkout/', views.checkout_view, name='billing_checkout'),
    
    # Secure API endpoint to receive and process JSON checkout carts
    path('checkout/process/', views.process_transaction, name='process_transaction'),
]
