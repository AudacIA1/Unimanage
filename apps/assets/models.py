from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone

class AssetCategory(MPTTModel):
    """
    Representa una categoría jerárquica para los activos.
    Utiliza django-mptt para gestionar la estructura de árbol, permitiendo
    categorías y subcategorías anidadas.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True, help_text="Descripción de la categoría.")
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="Nombre del ícono (ej. 'fas fa-laptop').")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Categoría de Activo"
        verbose_name_plural = "Categorías de Activos"

    def __str__(self):
        """Representación en cadena de la categoría."""
        return self.name


class Asset(models.Model):
    """
    Representa un activo físico o digital en el inventario de la universidad.
    Cada activo tiene un código único, pertenece a una categoría y tiene un estado.
    """
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_uso', 'En uso'),
        ('mantenimiento', 'En mantenimiento'),
    ]
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True, blank=True, null=True, editable=False)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, related_name="assets")
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponible')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_available(self, start=None, end=None):
        """
        Verifica si el activo está disponible en un rango de fechas.
        Un activo está disponible si su estado es 'disponible' y no está
        reservado para un evento que se solape con el rango de fechas.

        Args:
            start (datetime, optional): Fecha de inicio del rango. Defaults to None.
            end (datetime, optional): Fecha de fin del rango. Defaults to None.

        Returns:
            bool: True si el activo está disponible, False en caso contrario.
        """
        # Primero, verifica el estado general del activo
        if self.status != 'disponible':
            return False

        # Si el estado es 'disponible', verifica si hay reservas de eventos que se solapen
        if start is None:
            start = timezone.now()
        if end is None:
            end = start
        overlapping = self.events_reserved_for.filter(
            fecha_inicio__lt=end,
            fecha_fin__gt=start,
            status__in=['approved','active']
        )
        return not overlapping.exists()

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para generar un código de activo único
        la primera vez que se crea el objeto.
        El código se forma con el prefijo de la categoría y el ID del activo.
        """
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new and not self.code:
            prefix = self.category.name[:3].upper() if self.category else 'GEN'
            self.code = f'{prefix}-{self.pk:05d}'
            Asset.objects.filter(pk=self.pk).update(code=self.code)

    def __str__(self):
        """Representación en cadena del activo."""
        return f"{self.name} ({self.code})"
