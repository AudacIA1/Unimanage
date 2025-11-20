"""
Define las rutas URL para la aplicación de cuentas, incluyendo registro, inicio de sesión,
cierre de sesión y una vista para manejar la falta de permisos.
"""
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='dashboard_home'), name='logout'),
    path('no_permission/', views.no_permission_view, name='no_permission'),
]