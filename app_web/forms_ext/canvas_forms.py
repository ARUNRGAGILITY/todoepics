from django import forms
from ..models import OpsTransformationCanvas

class OpsTransformationCanvasForm(forms.ModelForm):
    class Meta:
        model = OpsTransformationCanvas
        fields = ['name', 'description', 'ops_value_stream', 'docs']
        widgets = {
            'name': forms.TextInput(attrs={'size': '50',}),
            'description': forms.Textarea(attrs={ 'rows': 4, 'cols': 40}),
            'docs': forms.Textarea(attrs={ 'rows': 4, 'cols': 40}),
        }