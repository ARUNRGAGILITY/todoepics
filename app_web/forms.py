from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from .models import Role
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
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
