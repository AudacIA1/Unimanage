from django import forms
from .models import Maintenance
from apps.assets.models import Asset
from dal import autocomplete

class MaintenanceForm(forms.ModelForm):
    """
    Formulario para la creación y edición de tareas de mantenimiento.
    
    Utiliza el modelo `Maintenance` y personaliza los widgets para
    mejorar la experiencia de usuario.
    """
    asset = forms.ModelChoiceField(
        queryset=Asset.objects.filter(status='disponible'),
        widget=autocomplete.ModelSelect2(
            url='asset-autocomplete',
            attrs={
                'data-placeholder': 'Buscar un activo disponible...',
                'data-minimum-input-length': 1,
            }
        )
    )

    class Meta:
        model = Maintenance
        fields = ["asset", "description", "performed_by", "status"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Describa el trabajo de mantenimiento a realizar"}),
            "performed_by": forms.TextInput(attrs={"placeholder": "Nombre del técnico o empresa"}),
        }

    def __init__(self, *args, **kwargs):
        super(MaintenanceForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['asset'].queryset = Asset.objects.all()
            self.fields['asset'].widget.url = '/activos/asset-autocomplete-all/'