from django.db import models
from django.contrib.auth import get_user_model
from apps.assets.models import Asset # Importar el modelo Asset

User = get_user_model()

from mptt.models import MPTTModel, TreeForeignKey

class AttendingEntity(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class Evento(models.Model):
    TIPO_CHOICES = [
        ('evento', 'Evento'),
        ('visita', 'Visita'),
        ('prestamo', 'Préstamo'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
        ('active', 'Activo'),
    ]

    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='evento')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    lugar = models.CharField(max_length=200, blank=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    attending_entity = TreeForeignKey(AttendingEntity, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    reserved_assets = models.ManyToManyField(Asset, blank=True, related_name='events_reserved_for') # Nuevo campo

    class Meta:
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"

class ChecklistItem(models.Model): # Nuevo modelo
    event = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='checklist_items')
    description = models.TextField() # Changed from CharField to TextField
    is_checked = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, blank=False, null=False) # New field for ordering

    def __str__(self):
        return f"{self.description} ({'Checked' if self.is_checked else 'Unchecked'})"
