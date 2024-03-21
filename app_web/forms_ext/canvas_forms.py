from django import forms
from ..models import *

class OpsTransformationCanvasForm(forms.ModelForm):
    class Meta:
        model = OpsTransformationCanvas
        fields = ['name', 'description', 'opsvaluestream',  'demand_rate','boundaries_and_constraints', 'improvement_items', ]
        widgets = {
            'name': forms.TextInput(attrs={'size': '50',}),
            'description': forms.Textarea(attrs={ 'rows': 4, 'cols': 40}),
            'docs': forms.Textarea(attrs={ 'rows': 4, 'cols': 40}),
            'demand_rate': forms.TextInput(attrs={'size': '50',}),
            'boundaries_and_constraints': forms.Textarea(attrs={'cols': 30, 'rows': 5}),
            'improvement_items': forms.Textarea(attrs={'cols': 30, 'rows': 5}),
        }
        
class DevTransformationCanvasForm(forms.ModelForm):
    class Meta:
        model = DevTransformationCanvas
        fields = ['name', 'description', 'devvaluestream' , 'demand_rate','boundaries_and_constraints', 'improvement_items', ]
        widgets = {
            'name': forms.TextInput(attrs={'size': '50',}),
            'description': forms.Textarea(attrs={ 'rows': 4, 'cols': 40}),
            'docs': forms.Textarea(attrs={ 'rows': 4, 'cols': 40}),
            'demand_rate': forms.TextInput(attrs={'size': '50',}),
            'boundaries_and_constraints': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
            'improvement_items': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        
class EditDevTransformationCanvasForm(forms.ModelForm):
    class Meta:
        model = DevTransformationCanvas
        fields = ['name', 'description', 'devvaluestream' ,]
        widgets = {
            'name': forms.TextInput(attrs={'size': '50',}),
            'description': forms.Textarea(attrs={ 'rows': 4, 'cols': 40}),
        }
        
