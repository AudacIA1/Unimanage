from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

class AssetCategory(MPTTModel):
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
        return self.name


class Asset(models.Model):
    """
    Representa un activo individual en el inventario.
    
    Cada activo tiene un nombre, una categoría, una ubicación y un estado.
    También registra cuándo fue creado y actualizado.
    """
    name = models.CharField(max_length=100)
    asset_code = models.CharField(
        max_length=255, 
        unique=True, 
        blank=True, 
        null=True, 
        editable=False, 
        help_text="Código único para el activo, generado automáticamente."
    )
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, related_name="assets")
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[
        ("Disponible", "Disponible"),
        ("En uso", "En uso"),
        ("En mantenimiento", "En mantenimiento"),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método de guardado para generar un `asset_code` único
        la primera vez que se crea el objeto.
        """
        # El código se genera solo en la primera creación del objeto.
        is_new = self._state.adding
        # Se guarda el objeto primero para obtener un ID (pk) asignado por la base de datos.
        super().save(*args, **kwargs)
        # Si es un objeto nuevo y aún no tiene un asset_code...
        if is_new and not self.asset_code:
            # Se usa el prefijo de la categoría (si existe) y el ID del objeto.
            prefix = self.category.name[:3].upper() if self.category else 'GEN'
            self.asset_code = f'{prefix}-{self.pk:05d}'
            # Se actualiza el objeto de nuevo, pero usando .update() para evitar
            # una llamada recursiva al método save().
            Asset.objects.filter(pk=self.pk).update(asset_code=self.asset_code)

    def __str__(self):
        """Devuelve el nombre del activo."""
        return self.name
