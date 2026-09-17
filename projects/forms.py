from django import forms
from django.forms import inlineformset_factory

from django.urls import reverse_lazy
from .models import EquipmentHistory, Project, Equipment, EquipmentSupplier, EquipmentType, Task, BoqItem
from inventory.models import Inventory


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "project_no",
            "client",
            "project_title",
            "project_type",
            "location",
            "start_date",
            "scope_of_work",
            "work_status",
            "work_status_detail",
            "remaining_work",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "scope_of_work": forms.Textarea(attrs={"rows": 5}),
            "remaining_work": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["work_status"].widget.attrs["class"] = "form-select"
        self.fields["project_type"].widget.attrs["class"] = "form-select"
        self.fields["scope_of_work"].help_text = "Describe the agreed work and deliverables."
        self.fields["remaining_work"].help_text = "Record incomplete work, dependencies, or next actions."


class EquipmentSupplierForm(forms.ModelForm):
    class Meta:
        model = EquipmentSupplier
        fields = ['supplier_name', 'supplier_address', 'supplier_phone', 'supplier_email', 'contact_person', 'contact_person_phone', 'contact_person_email', 'equipment_rent']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["supplier_address"].help_text = "Full address of the supplier."

class EquipmentTypeForm(forms.ModelForm):
    class Meta:
        model= EquipmentType
        fields = ['equipment_type', 'equipment_properties']

        widgets = {
            "equipment_properties": forms.Textarea(attrs={"rows": 3}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["equipment_properties"].help_text = "Mention total height, platform height etc."

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [ 'equipment_no', 'equipment_slno', 'equipment_type', 'equipment_manufacture', 'equipment_status']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["equipment_status"].widget.attrs["class"] = "form-select"

class EquipmentHistoryForm(forms.ModelForm):
    class Meta:
        model = EquipmentHistory
        fields = ["entry_date", "equipment", "activity", "quantity", "notes"]
        widgets = {
            "entry_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["equipment"].widget.attrs["class"] = "form-select"

EquipmentHistoryFormSet = inlineformset_factory(
    Project,
    EquipmentHistory,
    form=EquipmentHistoryForm,
    extra=1,
    can_delete=True,
)


class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            "entry_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

ProjectTaskFormSet = inlineformset_factory(
    Project,
    Task,
    form=ProjectTaskForm,
    extra=1,
    can_delete=True,
)


# class AddBoqForm(forms.ModelForm):
#     class Meta:
#         model = BoqItem
#         fields = ['boq_category', 'boq_item', 'boq_size', 'boq_uom', 'boq_qty']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs.setdefault("class", "form-control")

class AddBoqForm(forms.ModelForm):
    class Meta:
        model = BoqItem
        fields = ['boq_category', 'boq_item', 'boq_size', 'boq_uom', 'boq_qty']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        
        # HTMX attributes (Removed hx-vals, changed target ID to match Django's default id)
        self.fields['boq_category'].widget.attrs.update({
            'hx-get': reverse_lazy('projects:ajax_load_inventory_items'), 
            'hx-trigger': 'change',                                      
            'hx-target': '#id_boq_item',  # Default Django HTML ID format                               
        })

        if 'boq_category' not in self.data:
            self.fields['boq_item'].queryset = Inventory.objects.none()
        elif self.data.get('boq_category'):
            self.fields['boq_item'].queryset = Inventory.objects.filter(category_id=self.data.get('boq_category'))
