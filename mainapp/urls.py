from django.urls import path
from . import views

urlpatterns = [
    path('user/<str:pk>/', views.user_dashboard, name='user_dashboard'),
    path('admin_/', views.admin_dashboard, name='admin_dashboard'),
]
