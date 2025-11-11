from django.conf import settings
from django.utils import timezone
from django.db import models
from datetime import datetime

class Loan(models.Model):
    """
    Representa un préstamo de un activo a un usuario.

    Registra qué activo fue prestado, a qué usuario, las fechas del
    préstamo y devolución, y el estado actual del préstamo.
    """
    asset = models.ForeignKey("assets.Asset", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=datetime(2030, 1, 1, 0, 0, 0))
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ("Activo", "Activo"),
        ("Devuelto", "Devuelto"),
    ])

    def __str__(self):
        """Devuelve una representación en string del préstamo."""
        return f"{self.asset.name} → {self.user.username}"

    @property
    def is_overdue(self):
        return self.status == 'Activo' and self.due_date < timezone.now()