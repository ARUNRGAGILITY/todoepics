from ..all_form_imports import *

from ...models.list.model_list import *
from ...models.permission.model_permission import *


# Generic Permission
class GenericPermissionForm(forms.ModelForm):
    class Meta:
        model = GenericPermission
        fields = ['user', 'group', 'permission']
