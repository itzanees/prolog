from django import forms
from django.forms import inlineformset_factory

from .models import Supplier, Category, Uom, Inventory

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name','address','phone','email', 'cr_no', 'vat_id', 'bank_name', 'bank_account_no', 'bank_iban_no'
            ]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
       
class UomForm(forms.ModelForm):
    class Meta:
        model = Uom
        fields = ['uom', 'symbol']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = [
            'category','item','length', 'width','uom','supplier','qty'
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'category_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
       