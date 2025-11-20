from django.db import models
from apps.assets.models import Asset
from django.utils import timezone
from django.contrib.auth.models import User

class Maintenance(models.Model):
    """
    Representa una tarea de mantenimiento programada o realizada para un activo.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En progreso'),
        ('completed', 'Completado'),
    ]
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    performed_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        """Devuelve una representación en string del mantenimiento."""
        return f"{self.asset.name} - {self.get_status_display()} ({self.created_at.date()})"