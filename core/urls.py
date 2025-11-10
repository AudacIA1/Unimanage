"""
URL configuration for unimanage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
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
