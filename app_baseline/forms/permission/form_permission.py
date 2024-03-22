from ..all_form_imports import *

from ...models.list.model_list import *
from ...models.permission.model_permission import *


class PermissionForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False,
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=CustomGroup.objects.filter(active=True),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False,
    )
    inherit = forms.BooleanField(required=False)
    users_can_view = forms.BooleanField(required=False)
    can_view = forms.BooleanField(required=False)
    can_add = forms.BooleanField(required=False)
    can_change = forms.BooleanField(required=False)
    can_delete = forms.BooleanField(required=False)

    class Meta:
        model = Permission
        fields = ['users', 'groups', 'inherit', 'users_can_view', 'can_view', 'can_add', 'can_change', 'can_delete']
    
    def clean_users(self):
        data = self.cleaned_data['users']
        print(f"Data before cleaning: {data}")  # Debugging line
        if data == '' or data is None:
            print("Data is empty or None. Setting it to None.")
            return None
        print(f"Data after cleaning: {data}")
        return data


class ListPermissionForm(forms.ModelForm):
   
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False,
        label='Users'
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False,
        label='Groups'
    )
    inherit = forms.BooleanField(
        required=False,
        label='Inherit'
    )
    users_can_view = forms.BooleanField(
        required=False,
        label='Users Can View'
    )
    can_view = forms.BooleanField(
        required=False,
        label='Can View'
    )
    can_add = forms.BooleanField(
        required=False,
        label='Can Add'
    )
    can_change = forms.BooleanField(
        required=False,
        label='Can Change'
    )
    can_delete = forms.BooleanField(
        required=False,
        label='Can Delete'
    )
    
    class Meta:
        model = ListPermission
        fields = [

            'users',
            'groups',
            'inherit',
            'users_can_view',
            'can_view',
            'can_add',
            'can_change',
            'can_delete'
        ]




# class PermissionForm(forms.ModelForm):
#     users = forms.ModelMultipleChoiceField(
#         queryset=User.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )
#     groups = forms.ModelMultipleChoiceField(
#         queryset=Group.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )
#     inherit = forms.BooleanField(required=False)
#     users_can_view = forms.BooleanField(required=False)
#     can_view = forms.BooleanField(required=False)
#     can_add = forms.BooleanField(required=False)
#     can_change = forms.BooleanField(required=False)
#     can_delete = forms.BooleanField(required=False)

#     class Meta:
#         model = Permission
#         fields = ['users', 'groups', 'inherit', 'users_can_view', 'can_view', 'can_add', 'can_change', 'can_delete']
