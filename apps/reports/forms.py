from django import forms
from apps.assets.models import AssetCategory, Asset # Import Asset to get distinct locations
from django.contrib.auth import get_user_model # Import User model if needed for other reports

class AssetUsageFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False, 
        label="Desde", 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input rounded-md shadow-sm'})
    )
    end_date = forms.DateField(
        required=False, 
        label="Hasta", 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input rounded-md shadow-sm'})
    )
    category = forms.ModelChoiceField(
        queryset=AssetCategory.objects.all(), 
        required=False, 
        label="Categoría",
        widget=forms.Select(attrs={'class': 'form-select rounded-md shadow-sm'})
    )
    
    # Dynamically get distinct locations from Asset model
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        location_choices = [(loc, loc) for loc in Asset.objects.values_list('location', flat=True).distinct() if loc]
        self.fields['location'] = forms.ChoiceField(
            choices=[('', 'Todas')] + location_choices, 
            required=False, 
            label="Ubicación",
            widget=forms.Select(attrs={'class': 'form-select rounded-md shadow-sm'})
        )
