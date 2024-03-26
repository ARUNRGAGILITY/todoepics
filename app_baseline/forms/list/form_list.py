from ..all_form_imports import *

from ...models.list.model_list import *
from ...models.permission.model_permission import *
class CustomTreeNodeChoiceField(TreeNodeChoiceField):
    def label_from_instance(self, obj):
        level = obj.get_level()

        # Customize how you want to display the hierarchical depth.
        # The following uses two spaces per depth level instead of hyphens.
        return ' ' * 2 * level + str(obj)
class ListForm(forms.ModelForm):

    def __init__(self, user, current_parent_id=None, *args, **kwargs):
        
        type_type_filter = kwargs.pop('type_type_filter', 'General') # TYPETYPE
        type_type = TypeType.objects.get(title=type_type_filter, active=True)

        super(ListForm, self).__init__(*args, **kwargs)
        self.user = user
        self.current_parent_id = current_parent_id
        self.fields['parent'].queryset = List.objects.filter(active=True)  # or filter based on some condition
        self.fields['parent'].required = False
        self.fields['description'].required = False
        self.fields['active'].required = False
        self.fields['deleted'].required = False

        # begin separating the positional arguments for additional information
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = None

        # experiment with the selected workitem and mapped config relevant type 
        if current_parent_id:
            current_instance = List.objects.get(active=True, id=current_parent_id)
            if current_instance.type:
                mapping_details = Type.objects.get(active=True, id=current_instance.type.id,
                                                   type_type=type_type.id)
                mapping_childrens = mapping_details.children()
                self.fields['type'] = CustomTreeNodeChoiceField(
                    queryset=mapping_childrens,
                    label='Select a Type',
                    empty_label='--Select type --'
                )
                self.fields['type'].required = False
                self.fields['type'].empty_label = '--Select type--'
                
        else:
            self.fields['type'] = CustomTreeNodeChoiceField(
            queryset=Type.objects.filter(active=True, parent=None, type_type=type_type.id).order_by('position'),
            label='Select a Type',
            empty_label='--Select type --'
            )
            self.fields['type'].required = False
            self.fields['type'].empty_label = '--Select type--'
        

        # self.fields['parent'] = TreeNodeChoiceField(
        #     queryset=List.objects.filter(active=True, user=user),
        #     label='Select a parent',
        #     empty_label='--Select parent --'
        # )
        # self.fields['parent'].required = False
        # self.fields['parent'].empty_label = '--Select parent--'        

    def clean_parent(self):
        parent = self.cleaned_data['parent']
        if parent is None:
            return None
        if parent == self.instance:
            raise forms.ValidationError("A node may not be made a child of itself.")
        return parent
    
    class Meta:
        model = List
        fields = ['parent', 'title', 'type', 'description', 'active', 'deleted' ]


### edit form

class EditListForm(forms.ModelForm):
    details = None
    parent = TreeNodeChoiceField(queryset=List.objects.filter(active=True), required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)

    def __init__(self, user, current_parent_id=None, *args, **kwargs):

        # begin separating the positional arguments for additional information
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = None

        super().__init__(data=data, *args, **kwargs)
        self.user = user
        self.current_parent_id = current_parent_id
        # end separating the positional arguments for additonal information

        
        self.fields['type'] = CustomTreeNodeChoiceField(
        queryset=Type.objects.filter(active=True, parent=None),
        label='Select a Type',
        empty_label='--Select type --'
        )
        self.fields['type'].required = False
        self.fields['type'].empty_label = '--Select type--'
        

        self.fields['parent'] = CustomTreeNodeChoiceField(
            queryset=List.objects.filter(active=True, ),
            label='Select a parent',
            empty_label='--Select parent --'
        )
        self.fields['parent'].required = False
        self.fields['parent'].empty_label = '--Select parent--'

        

    def clean_parent(self):
        parent = self.cleaned_data['parent']
        if parent is None:
            return None
        if parent == self.instance:
            raise forms.ValidationError("A node may not be made a child of itself.")
        return parent
    
    
    
    class Meta:
        model = List
        fields = ['parent', 'title', 'type', 'description' ]