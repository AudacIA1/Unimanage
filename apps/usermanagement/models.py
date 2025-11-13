from django.db import models
from django.conf import settings

# Create your models here.
class DashboardPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prefs = models.JSONField(default=dict)  # { order: [...], visible: {...} }
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Prefs {self.user}'