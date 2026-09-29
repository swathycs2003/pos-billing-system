from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    # Main dashboard panel view URL
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
