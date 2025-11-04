from django import forms
from .models import LoanRequest

class AssetRequestForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    class Meta:
        model = LoanRequest
        fields = ['asset', 'start_date', 'end_date', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows':3}),
        }
