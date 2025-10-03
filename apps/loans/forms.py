from django import forms
from .models import Loan
from dal import autocomplete
from apps.assets.models import Asset

class LoanForm(forms.ModelForm):
    """
    Formulario para la creación y edición de préstamos.
    
    Utiliza un widget de autocompletado para el campo 'asset' para
    facilitar la búsqueda de activos disponibles.
    """
    asset = forms.ModelChoiceField(
        queryset=Asset.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='asset-autocomplete',
            attrs={
                'data-placeholder': 'Buscar un activo disponible...',
                'data-minimum-input-length': 1,
            }
        )
    )

    class Meta:
        model = Loan
        fields = ["asset", "user", "return_date", "status"]