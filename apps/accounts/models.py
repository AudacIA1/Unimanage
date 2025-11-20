from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    """
    Extiende el modelo de usuario predeterminado de Django con información adicional
    específica del perfil, como el rol, número de teléfono y departamento.
    """
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('tech', 'Técnico'),
        ('staff', 'Administrativo'),
        ('user', 'Usuario'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile',
        help_text="El usuario de Django asociado a este perfil."
    )
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='user',
        help_text="Rol del usuario dentro del sistema (ej. Administrador, Técnico)."
    )
    phone = models.CharField(
        max_length=30, 
        blank=True, 
        null=True,
        help_text="Número de teléfono del usuario."
    )
    department = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Departamento o facultad al que pertenece el usuario."
    )

    def __str__(self):
        """
        Representación en cadena del perfil de usuario.
        Muestra el nombre de usuario y su rol.
        """
        return f"{self.user.username} — {self.get_role_display()}"
