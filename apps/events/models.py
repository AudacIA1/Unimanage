from django.db import models
from django.contrib.auth import get_user_model
from apps.assets.models import Asset # Importar el modelo Asset

User = get_user_model()

from mptt.models import MPTTModel, TreeForeignKey

class AttendingEntity(MPTTModel):
    """
    Representa una entidad que puede asistir o estar relacionada con un evento.
    Utiliza django-mptt para permitir una estructura jerárquica de entidades.
    """
    name = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Nombre de la entidad asistente."
    )
    parent = TreeForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        help_text="Entidad padre en la jerarquía."
    )

    class MPTTMeta:
        """Opciones de configuración para MPTT."""
        order_insertion_by = ['name']

    def __str__(self):
        """Representación en cadena de la entidad asistente."""
        return self.name

class Evento(models.Model):
    """
    Representa un evento, visita o préstamo que ocurre en la universidad.
    Incluye detalles como título, descripción, tipo, fechas, lugar, responsable
    y activos reservados.
    """
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

    titulo = models.CharField(
        max_length=150,
        help_text="Título o nombre del evento."
    )
    descripcion = models.TextField(
        blank=True,
        help_text="Descripción detallada del evento."
    )
    tipo = models.CharField(
        max_length=10, 
        choices=TIPO_CHOICES, 
        default='evento',
        help_text="Tipo de evento (Evento, Visita, Préstamo)."
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        help_text="Estado actual del evento (Pendiente, Aprobado, Rechazado, Activo)."
    )
    fecha_inicio = models.DateTimeField(
        help_text="Fecha y hora de inicio del evento."
    )
    fecha_fin = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Fecha y hora de finalización del evento (opcional)."
    )
    lugar = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Lugar donde se realizará el evento."
    )
    responsable = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Usuario responsable de la organización del evento."
    )
    attending_entity = TreeForeignKey(
        AttendingEntity, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Entidad o grupo que asiste al evento."
    )
    creado_en = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de creación del registro del evento."
    )
    reserved_assets = models.ManyToManyField(
        Asset, 
        blank=True, 
        related_name='events_reserved_for',
        help_text="Activos reservados para este evento."
    )
    max_attendees = models.IntegerField(
        null=True, 
        blank=True,
        help_text="Número máximo de asistentes permitidos (opcional)."
    )
    current_attendees = models.IntegerField(
        default=0, 
        null=True, 
        blank=True,
        help_text="Número actual de asistentes registrados."
    )

    class Meta:
        """Opciones de metadatos para el modelo."""
        ordering = ['-fecha_inicio']

    def __str__(self):
        """Representación en cadena del evento."""
        return f"{self.titulo} ({self.get_tipo_display()})"

class ChecklistItem(models.Model):
    """
    Representa un elemento de una lista de verificación asociada a un evento.
    Útil para tareas de preparación o seguimiento del evento.
    """
    event = models.ForeignKey(
        Evento, 
        on_delete=models.CASCADE, 
        related_name='checklist_items',
        help_text="Evento al que pertenece este elemento de la lista de verificación."
    )
    description = models.TextField(
        help_text="Descripción del elemento de la lista de verificación."
    )
    is_checked = models.BooleanField(
        default=False,
        help_text="Indica si el elemento de la lista de verificación ha sido completado."
    )
    order = models.PositiveIntegerField(
        default=0, 
        blank=False, 
        null=False,
        help_text="Orden en que aparece el elemento en la lista de verificación."
    )

    def __str__(self):
        """Representación en cadena del elemento de la lista de verificación."""
        return f"{self.description} ({'Checked' if self.is_checked else 'Unchecked'})"
