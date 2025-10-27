from django.db import models
from django.contrib.auth.models import User
from apps.assets.models import Asset

class LoanRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobada'),
        ('rejected', 'Rechazada'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_requests')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='loan_requests')
    reason = models.TextField(blank=True, null=True, verbose_name="Motivo de la solicitud")
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_comment = models.TextField(blank=True, null=True)
    response_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Solicitud de {self.user.username} - {self.asset.name} ({self.status})"
