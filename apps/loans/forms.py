from django import forms
from .models import Loan
from dal import autocomplete
from apps.assets.models import Asset
from django.utils import timezone # Import timezone

class LoanForm(forms.ModelForm):
    """
    Formulario para la creación y edición de préstamos.
    
    Utiliza un widget de autocompletado para el campo 'asset' para
    facilitar la búsqueda de activos disponibles.
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
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        initial=timezone.now() + timezone.timedelta(days=7) # Default to 7 days from now
    )

    class Meta:
        model = Loan
        fields = ["asset", "user", "due_date"]

class LoanEditForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["asset", "user", "due_date", "return_date", "status"]