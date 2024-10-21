from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'street_address', 'suburb', 'city', 'postal_code', 'region', 'country', 'business_name', 'gst_number']
