from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.user_login),
    path('user/<str:user_name>/', views.user_dashboard, name='user_dashboard'),
    path("user_dash_plot/<str:user_name>/", views.user_dash_plot, name="user_dash"),
    path('admin_/', views.admin_dashboard, name='admin_dashboard'),
    path("addtrader/", views.bgTransaction),
]
