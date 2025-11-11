from django import forms
from .models import Asset, AssetCategory
from mptt.forms import TreeNodeChoiceField
from dal import autocomplete # Import autocomplete

class AssetForm(forms.ModelForm):
    """
    Formulario para la creación y edición de activos.
    
    Utiliza el modelo `Asset` y personaliza los widgets para que
    tengan una clase CSS estándar para el estilo.
    """
    category = forms.ModelChoiceField(
        queryset=AssetCategory.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete',
                                         attrs={'data-placeholder': 'Search for a category',
                                                'data-minimum-input-length': 2})
    )

    class Meta:
        model = Asset
        fields = ["name", "category", "location", "status"]

    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk and hasattr(self.instance, 'loan_set') and self.instance.loan_set.filter(status='Activo').exists():
            self.fields['status'].disabled = True

class AssetCategoryForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=AssetCategory.objects.all(),
                                 level_indicator='---',
                                 required=False, # Parent can be null
                                 )
    class Meta:
        model = AssetCategory
        fields = ['name', 'parent']