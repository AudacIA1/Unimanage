"""
Configuración de URL principal para el proyecto UniManage.

Define las rutas a las aplicaciones principales del sistema, incluyendo
administración de Django, cuentas de usuario, dashboard, gestión de activos,
préstamos, mantenimientos, reportes, chatbot, gestión de usuarios, eventos y solicitudes.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings # Added this line

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")), # Include accounts app URLs
    path("", include("apps.dashboard.urls")),         # Dashboard principal
    path("activos/", include("apps.assets.urls")),  # CRUD de activos
    path("prestamos/", include("apps.loans.urls")), # Gestión de préstamos
    path("mantenimientos/", include("apps.maintenance.urls")), # Gestión de mantenimientos
    path("reportes/", include(("apps.reports.urls", "reports"), namespace="reports")), # Reportes
    
    path("chatbot/", include("apps.chatbot.urls")), # Chatbot URLs
    path("usuarios/", include("apps.usermanagement.urls")), # User Management URLs
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico')),
    path('eventos/', include(('apps.events.urls', 'events'), namespace='events')),
    path('solicitudes/', include('apps.request.urls', namespace='request')),


]
