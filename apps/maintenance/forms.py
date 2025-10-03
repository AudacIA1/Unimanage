from django import forms
from .models import Maintenance

class MaintenanceForm(forms.ModelForm):
    """
    Formulario para la creación y edición de tareas de mantenimiento.
    
    Utiliza el modelo `Maintenance` y personaliza los widgets para
    mejorar la experiencia de usuario.
    """
    class Meta:
        model = Maintenance
        fields = ["asset", "description", "performed_by", "status"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }