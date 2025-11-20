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
    asset = models.ForeignKey(
        "assets.Asset", 
        on_delete=models.CASCADE,
        help_text="El activo que ha sido prestado."
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="El usuario al que se le prestó el activo."
    )
    loan_date = models.DateTimeField(
        default=timezone.now,
        help_text="Fecha y hora en que se realizó el préstamo."
    )
    due_date = models.DateTimeField(
        default=datetime(2030, 1, 1, 0, 0, 0),
        help_text="Fecha y hora límite para la devolución del activo."
    )
    return_date = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Fecha y hora en que el activo fue devuelto (si aplica)."
    )
    status = models.CharField(
        max_length=20, 
        choices=[
            ("Activo", "Activo"),
            ("Devuelto", "Devuelto"),
        ],
        help_text="Estado actual del préstamo (Activo o Devuelto)."
    )

    def __str__(self):
        """Devuelve una representación en string del préstamo."""
        return f"{self.asset.name} → {self.user.username}"

    @property
    def is_overdue(self):
        """
        Indica si el préstamo está vencido.
        Un préstamo está vencido si su estado es 'Activo' y la fecha de vencimiento
        es anterior a la fecha y hora actuales.
        """
        return self.status == 'Activo' and self.due_date < timezone.now()