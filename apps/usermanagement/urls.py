"""
Define las rutas URL para la aplicación de gestión de usuarios, incluyendo
operaciones CRUD para usuarios y un endpoint de API para preferencias del dashboard.
"""
# usermanagement/urls.py
from django.urls import path
from .views import UserListView, UserCreateView, UserUpdateView, UserDeleteView
from .api import dashboard_preferences

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('crear/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/editar/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/eliminar/', UserDeleteView.as_view(), name='user_delete'),
    path('api/dashboard/preferences/', dashboard_preferences, name='dashboard_preferences'),
]
