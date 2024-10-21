from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'street_address', 'suburb', 'city', 'postal_code', 'region', 'country', 'business_name', 'gst_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round'}),
            'email': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round'}),
            'phone': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round'}),
            'street_address': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round'}),
            'suburb': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round'}),
            'city': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round'}),
            'postal_code': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round'}),
            'region': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round'}),
            'country': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round'}),
            'business_name': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round'}),
            'gst_number': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round'}),
        }
