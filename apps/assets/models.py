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


from django.utils import timezone

class Asset(models.Model):
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
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new and not self.code:
            prefix = self.category.name[:3].upper() if self.category else 'GEN'
            self.code = f'{prefix}-{self.pk:05d}'
            Asset.objects.filter(pk=self.pk).update(code=self.code)

    def __str__(self):
        return f"{self.name} ({self.code})"


