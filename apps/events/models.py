from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Evento(models.Model):
    TIPO_CHOICES = [
        ('evento', 'Evento'),
        ('visita', 'Visita'),
    ]

    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='evento')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    lugar = models.CharField(max_length=200, blank=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    visitante = models.CharField(max_length=200, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"
