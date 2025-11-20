"""
Define las rutas URL para la aplicación de solicitudes de préstamo, incluyendo
listado, creación, detalle, aprobación, rechazo, eliminación de solicitudes
y búsqueda de activos.
"""
from django.urls import path
from . import views

app_name = 'request'

urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('crear/', views.request_create, name='request_create'),
    path('<int:pk>/', views.request_detail, name='request_detail'),
    path('<int:pk>/aprobar/', views.request_approve, name='request_approve'),
    path('<int:pk>/rechazar/', views.request_reject, name='request_reject'),
    path('<int:pk>/borrar/', views.request_delete, name='request_delete'),
    path('buscar/', views.search_assets, name='search_assets'),
]
