import json

from django import forms
from .models import Vendor, PurchaseOrder


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'
        # fields = ['name', 'contact_details', 'address', 'vendor_code']


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    def clean_items(self):
        items = self.cleaned_data.get('items')
        print(type(items))
        return items
