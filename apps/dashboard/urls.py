"""
Define las rutas URL para la aplicación del dashboard, incluyendo la vista principal
del dashboard y la funcionalidad de exportación de reportes.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard_home"),   # Vista principal
    path("export/", views.export_report, name="export_report"),
]