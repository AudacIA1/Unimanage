from django.db import models
from django.contrib.auth.models import User
from apps.assets.models import Asset

class LoanRequest(models.Model):
    """
    Representa una solicitud de préstamo de un activo por parte de un usuario.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobada'),
        ('rejected', 'Rechazada'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_requests')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='loan_requests')
    reason = models.TextField(blank=True, null=True, verbose_name="Motivo de la solicitud")
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_comment = models.TextField(blank=True, null=True)
    response_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """Representación en cadena de la solicitud de préstamo."""
        return f"Solicitud de {self.user.username} - {self.asset.name} ({self.status})"
