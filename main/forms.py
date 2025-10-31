from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['category', 'asset_type', 'name', 'description', 'price_per_day', 'image']

