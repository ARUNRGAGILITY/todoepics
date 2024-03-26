# Create a form for OVSTypes model
# Path: app_web/forms_ext/enabler_forms.py
from django import forms
from app_web.models import OVS_Types
class OVS_TypesForm(forms.ModelForm):
    class Meta:
        model = OVS_Types
        fields = '__all__'
