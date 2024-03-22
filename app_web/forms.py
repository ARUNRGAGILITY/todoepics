from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import User

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'description']

class OpsValueStreamForm(forms.ModelForm):
    class Meta:
        model = OpsValueStream
        fields = ['name', 'description']  


class OpsValueStreamForm(forms.ModelForm):
    trigger = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    value = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)


    class Meta:
        model = OpsValueStream
        fields = ['trigger', 'value', 'name', 'description', ]
        widgets = {
            'trigger': forms.TextInput(attrs={'size': '50',}),
            'value': forms.TextInput(attrs={'size': '50',}),
            'name': forms.TextInput(attrs={'size': '50',}),
            'description': forms.Textarea(attrs={'class': 'custom-css-class', 'rows': 4, 'cols': 40}),
        }

    

class DevValueStreamForm(forms.ModelForm):
    ops_valuestream_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    supported_ops_steps = forms.ModelMultipleChoiceField(
        queryset=ValueStreamSteps.objects.none(),  # Initial queryset will be dynamically set based on the instance
        required=False, 
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = DevValueStream
        fields = ['trigger', 'value','name', 'description', 'supported_ops_steps']
        widgets = {
            'trigger': forms.TextInput(attrs={'size': '50',}),
            'value': forms.TextInput(attrs={'size': '50',}),
            'name': forms.TextInput(attrs={'size': '50',}),
            'description': forms.Textarea(attrs={'class': 'custom-css-class', 'rows': 4, 'cols': 40}),
        }
        
    

    # def __init__(self, *args, **kwargs):
    #     super(DevValueStreamForm, self).__init__(*args, **kwargs)
        
    #     # Assuming 'instance' is a DevValueStream instance
    #     instance = kwargs.get('instance', None)
    #     if instance and instance.ops_valuestream:  # Check if this DevValueStream is related to an OpsValueStream
    #         # Directly filter ValueStreamSteps based on the ops_valuestream ForeignKey relation
    #         print(f">>> === {instance.ops_valuestream} testing form init === <<<")
    #         self.fields['supported_ops_steps'].queryset = ValueStreamSteps.objects.filter(
    #             opsvaluestream=instance.ops_valuestream,  # Adjust the field name if it's different
    #             active=True  # Assuming you want to filter by active steps
    #         )

    def __init__(self, *args, **kwargs):
        super(DevValueStreamForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)

        if instance and instance.ops_valuestream:
            ops_valuestream = instance.ops_valuestream
        else:
            # Attempt to set initial queryset based on hidden input or initial value
            ops_valuestream_id = self.initial.get('ops_valuestream_id') or self.data.get('ops_valuestream_id')
            try:
                ops_valuestream = OpsValueStream.objects.get(id=ops_valuestream_id)
            except (OpsValueStream.DoesNotExist, TypeError, ValueError):
                ops_valuestream = None

        if ops_valuestream:
            self.fields['supported_ops_steps'].queryset = ValueStreamSteps.objects.filter(
                opsvaluestream=ops_valuestream,
                active=True
            )
        else:
            self.fields['supported_ops_steps'].queryset = ValueStreamSteps.objects.none()
        
class ValueStreamStepsForm(forms.ModelForm):
    class Meta:
        model = ValueStreamSteps
        fields = ['name', 'description', 'owner', 'value_creation_time', 'delay_time', 'percentage_accurate']  
        widgets = {
            'description': forms.Textarea(attrs={'class': 'custom-css-class', 'rows': 4, 'cols': 40}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = AWProfile
        fields = ['bio', 'roles']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'custom-css-class', 'rows': 4, 'cols': 40}),
            'roles': forms.CheckboxSelectMultiple,
        }


class CustomUserCreationForm(UserCreationForm):
    roles = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), widget=forms.CheckboxSelectMultiple, required=False, help_text='Select roles')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'roles')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['roles'].queryset = Role.objects.all()
