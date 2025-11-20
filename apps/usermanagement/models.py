from django.db import models
from django.conf import settings

# Create your models here.
class DashboardPreference(models.Model):
    """
    Almacena las preferencias personalizadas del dashboard para cada usuario.
    Permite a los usuarios configurar la visibilidad y el orden de los elementos del dashboard.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="El usuario al que pertenecen estas preferencias."
    )
    prefs = models.JSONField(
        default=dict,
        help_text="Diccionario JSON que almacena las preferencias del dashboard (ej. orden, visibilidad)."
    )  # { order: [...], visible: {...} }
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha y hora de la última actualización de las preferencias."
    )

    def __str__(self):
        """Representación en cadena de las preferencias del dashboard."""
        return f'Prefs {self.user}'