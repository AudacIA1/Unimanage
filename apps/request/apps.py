from django.apps import AppConfig

class RequestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.request'
    verbose_name = 'Solicitudes de Préstamo'