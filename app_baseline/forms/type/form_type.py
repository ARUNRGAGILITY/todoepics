from ..all_form_imports import *
from ...models.type.model_type import *

class TypeForm(forms.ModelForm):
    details = None
    parent = TreeNodeChoiceField(queryset=Type.objects.filter(active=True), required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)

    def __init__(self, user, current_parent_id=None, *args, **kwargs):
        super(TypeForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['parent'] = TreeNodeChoiceField(
            queryset=Type.objects.filter(active=True, ),
            label='Select a source',
            empty_label='--Select source --'
        )
        self.fields['parent'].required = False
        self.fields['parent'].empty_label = '--Select source--'   

    def clean_parent(self):
        parent = self.cleaned_data['parent']
        if parent is None:
            return None
        if parent == self.instance:
            raise forms.ValidationError("A node may not be made a child of itself.")
        return parent
        
    class Meta:
        model = Type
        fields = ['parent', 'title','description' ]