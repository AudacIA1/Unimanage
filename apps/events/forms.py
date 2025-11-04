from django import forms
from django.forms import inlineformset_factory
from .models import Evento, ChecklistItem
from apps.assets.models import Asset # Importar el modelo Asset
from dal import autocomplete # Importar autocomplete

class EventoForm(forms.ModelForm):
    reserved_assets = forms.ModelMultipleChoiceField(
        queryset=Asset.objects.filter(status='disponible'),
        widget=autocomplete.ModelSelect2Multiple(url='asset-autocomplete'), # Usar widget de autocompletado
        required=False
    )

    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'tipo', 'fecha_inicio', 'fecha_fin', 'lugar', 'responsable', 'attending_entity', 'max_attendees', 'reserved_assets']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El queryset y el widget ahora se definen directamente en el campo, no es necesario configurarlos aquí
        # self.fields['reserved_assets'].queryset = Asset.objects.filter(status='disponible')
        # self.fields['reserved_assets'].widget = forms.CheckboxSelectMultiple()


class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['description', 'is_checked', 'order']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Descripción del ítem'}),
            'is_checked': forms.CheckboxInput(),
        }

ChecklistItemFormSet = inlineformset_factory(
    Evento,
    ChecklistItem,
    form=ChecklistItemForm,
    extra=1,
    can_delete=True,
)
