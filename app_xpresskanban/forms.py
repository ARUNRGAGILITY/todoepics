from django import forms
from .models import Project, Product, Service, Solution, ValueStream
from mptt.forms import TreeNodeChoiceField
from app_xpresskanban.models import *
from django.shortcuts import  get_object_or_404

class OrganizationForm(forms.ModelForm):    
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    type = forms.ModelChoiceField(queryset=BaseType.objects.filter(active=True), empty_label='Select Type', required=False)
    state = forms.ModelChoiceField(queryset=BaseState.objects.filter(active=True), empty_label='Select State', required=False)
    priority = forms.ModelChoiceField(queryset=BasePriority.objects.filter(active=True), empty_label='Select Priority', required=False)
    work_item_type = TreeNodeChoiceField(queryset=TYPE_HSDB.objects.filter(active=True), empty_label="Select a Work Item Type")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    progress = forms.DecimalField(max_digits=3, decimal_places=2, required=False)    
    current_state = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), required=False)
    done = forms.BooleanField(required=False)

    class Meta:
        model = Organization
        fields = [ 'title','description', 'type', 'state', 'priority', 'work_item_type', 'start_date', 'end_date', 'progress', 'current_state', 'done' ]



class ProjectForm(forms.ModelForm):    
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    type = forms.ModelChoiceField(queryset=BaseType.objects.filter(active=True), empty_label='Select Type', required=False)
    state = forms.ModelChoiceField(queryset=BaseState.objects.filter(active=True), empty_label='Select State', required=False)
    priority = forms.ModelChoiceField(queryset=BasePriority.objects.filter(active=True), empty_label='Select Priority', required=False)
    work_item_type = TreeNodeChoiceField(queryset=TYPE_HSDB.objects.filter(active=True), empty_label="Select a Work Item Type")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    progress = forms.DecimalField(max_digits=3, decimal_places=2, required=False)    
    current_state = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), required=False)
    done = forms.BooleanField(required=False)

    class Meta:
        model = Project
        fields = [ 'title','description', 'type', 'state', 'priority', 
                  'work_item_type', 'start_date', 'end_date','organization', 'progress', 'current_state', 'done' ]


class ProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    type = forms.ModelChoiceField(queryset=BaseType.objects.filter(active=True), empty_label='Select Type', required=False)
    state = forms.ModelChoiceField(queryset=BaseState.objects.filter(active=True), empty_label='Select State', required=False)
    priority = forms.ModelChoiceField(queryset=BasePriority.objects.filter(active=True), empty_label='Select Priority', required=False)
    work_item_type = TreeNodeChoiceField(queryset=TYPE_HSDB.objects.filter(active=True), empty_label="Select a Work Item Type")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    progress = forms.DecimalField(max_digits=3, decimal_places=2, required=False)    
    current_state = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), required=False)
    done = forms.BooleanField(required=False)

    class Meta:
        model = Product
        fields = [ 'title','description', 'type', 'state', 'priority', 
                  'work_item_type', 'start_date', 'end_date', 'organization', 'progress', 'current_state', 'done' ]

class ServiceForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    type = forms.ModelChoiceField(queryset=BaseType.objects.filter(active=True), empty_label='Select Type', required=False)
    state = forms.ModelChoiceField(queryset=BaseState.objects.filter(active=True), empty_label='Select State', required=False)
    priority = forms.ModelChoiceField(queryset=BasePriority.objects.filter(active=True), empty_label='Select Priority', required=False)
    work_item_type = TreeNodeChoiceField(queryset=TYPE_HSDB.objects.filter(active=True), empty_label="Select a Work Item Type")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    progress = forms.DecimalField(max_digits=3, decimal_places=2, required=False)    
    current_state = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), required=False)
    done = forms.BooleanField(required=False)

    class Meta:
        model = Service
        fields = [ 'title','description', 'type', 'state', 'priority', 
                  'work_item_type', 'start_date', 'end_date', 'organization', 'progress', 'current_state', 'done' ]


class SolutionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    type = forms.ModelChoiceField(queryset=BaseType.objects.filter(active=True), empty_label='Select Type', required=False)
    state = forms.ModelChoiceField(queryset=BaseState.objects.filter(active=True), empty_label='Select State', required=False)
    priority = forms.ModelChoiceField(queryset=BasePriority.objects.filter(active=True), empty_label='Select Priority', required=False)
    work_item_type = TreeNodeChoiceField(queryset=TYPE_HSDB.objects.filter(active=True), empty_label="Select a Work Item Type")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    progress = forms.DecimalField(max_digits=3, decimal_places=2, required=False)    
    current_state = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), required=False)
    done = forms.BooleanField(required=False)

    class Meta:
        model = Solution
        fields = [ 'title','description', 'type', 'state', 'priority',
                   'work_item_type', 'start_date', 'end_date','organization', 'progress', 'current_state', 'done' ]

class ValueStreamForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    type = forms.ModelChoiceField(queryset=BaseType.objects.filter(active=True), empty_label='Select Type', required=False)
    state = forms.ModelChoiceField(queryset=BaseState.objects.filter(active=True), empty_label='Select State', required=False)
    priority = forms.ModelChoiceField(queryset=BasePriority.objects.filter(active=True), empty_label='Select Priority', required=False)
    work_item_type = TreeNodeChoiceField(queryset=TYPE_HSDB.objects.filter(active=True), empty_label="Select a Work Item Type")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    progress = forms.DecimalField(max_digits=3, decimal_places=2, required=False)    
    current_state = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), required=False)
    done = forms.BooleanField(required=False)

    class Meta:
        model = ValueStream
        fields = [ 'title','description', 'type', 'state', 'priority',
                   'work_item_type', 'start_date', 'end_date','organization', 'progress', 'current_state', 'done' ]

class TeamForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    work_item_type = TreeNodeChoiceField(queryset=TYPE_HSDB.objects.filter(active=True), empty_label="Select a Work Item Type", required=False)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)    

    class Meta:
        model = Team
        fields = [ 'title','description', 
                   'organization',  ]

class BoardForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    done = forms.BooleanField(required=False)

    class Meta:
        model = Board
        fields = [ 'title','description',  'start_date', 'end_date',  'done' ]
        widgets = {'done': forms.CheckboxInput}


class BoardColumnsForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    policies = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    entry_criteria = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    exit_criteria = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    
    class Meta:
        model = BoardColumns
        fields = [ 'title','description','wip_limit' , 'policies', 'entry_criteria', 'exit_criteria']

class SwimlaneForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    
    class Meta:
        model = Swimlane
        fields = [ 'title','description', 'color']


from markdownx.models import MarkdownxField
class VMVSRIForm(forms.ModelForm):
    vision = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 20, 'cols': 80}), required=False)
    class Meta:
        model = VisionMissionValueSRI
        fields = [ 'vision',  ]

## for the user mgmt
class DeleteUserConfirmationForm(forms.Form):
    confirm = forms.BooleanField(required=True)

## for the group mgmt
class DeleteGroupConfirmationForm(forms.Form):
    confirm = forms.BooleanField(required=True)



#### preparing for the kanban board with CORE_HSDB
### TYPELIST FORM
### TYPELIST is a separate model to store the types, so that we can refer
class TYPE_HSDB_Form(forms.ModelForm):
    details = None
    parent = TreeNodeChoiceField(queryset=TYPE_HSDB.objects.filter(active=True), required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['parent'] = TreeNodeChoiceField(
            queryset=TYPE_HSDB.objects.filter(active=True, ),
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
        model = TYPE_HSDB
        fields = ['parent', 'title','description' ]

class CORE_HSDB_Form(forms.ModelForm):
    details = None
    parent = TreeNodeChoiceField(queryset=CORE_HSDB.objects.filter(active=True), required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    column = forms.ModelChoiceField(queryset=BoardColumns.objects.filter(active=True), required=False)
    swimlane = forms.ModelChoiceField(queryset=Swimlane.objects.filter(active=True), required=False)
    def __init__(self, user, current_parent_id=None, *args, **kwargs):

        # begin separating the positional arguments for additional information
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = None

        super().__init__(data=data, *args, **kwargs)
        self.user = user
        self.current_parent_id = current_parent_id

        # for column addition
        
        # Get the selected board instance from the form's instance (if available)
        selected_board = self.instance.board if self.instance else None
        # Set the queryset of the 'column' field based on the selected board
        if selected_board:
            self.fields['column'].queryset = BoardColumns.objects.filter(board=selected_board, active=True).order_by('position')
        else:
            self.fields['column'].queryset = BoardColumns.objects.none()  # No board selected, empty queryset

        # end column additions
        # for swimlane addition
        
        # Get the selected board instance from the form's instance (if available)
        selected_swimlane = self.instance.swimlane if self.instance else None
        # Set the queryset of the 'column' field based on the selected board
        if selected_swimlane:
            self.fields['swimlane'].queryset = Swimlane.objects.filter(board=selected_board,active=True).order_by('position')
        else:
            self.fields['swimlane'].queryset = Swimlane.objects.filter(board=selected_board,active=True).order_by('position')

        # end column additions

        # end separating the positional arguments for additonal information

        # experiment with the selected workitem and mapped config relevant type 
        if current_parent_id:
            print(f">>>>> FORM {current_parent_id} <<<<<<")
            current_instance = CORE_HSDB.objects.get(active=True, author=user, id=current_parent_id)
            print(f">>>>>> FORM WORK ITEM TYPE ===== {current_instance.workitemtype} <<<<<<")
            if current_instance.workitemtype:
                mapping_details = TYPE_HSDB.objects.get(active=True,  id=current_instance.workitemtype.id)
                mapping_childrens = mapping_details.children()
                print(f">>>>FORM>>>{mapping_childrens}")
                self.fields['workitemtype'] = TreeNodeChoiceField(
                    queryset=mapping_childrens,
                    label='Select a Type',
                    empty_label='--Select type --'
                )
                self.fields['workitemtype'].required = False
                self.fields['workitemtype'].empty_label = '--Select type--'
            
        else:
            print("=================== no PARENT ID GIVEN for FORM ================")
            self.fields['workitemtype'] = TreeNodeChoiceField(
            queryset=TYPE_HSDB.objects.filter(active=True),
            label='Select a Type',
            empty_label='--Select type --'
            )
            self.fields['workitemtype'].required = False
            self.fields['workitemtype'].empty_label = '--Select type--'
        

        self.fields['parent'] = TreeNodeChoiceField(
            queryset=CORE_HSDB.objects.filter(active=True, author=user),
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
        model = CORE_HSDB
        fields = ['parent', 'title', 'workitemtype', 'description', 'column', 'swimlane', 'done' ]

class Edit_CORE_HSDB_Form(forms.ModelForm):
    details = None
    parent = TreeNodeChoiceField(queryset=CORE_HSDB.objects.filter(active=True), required=False)
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

        
        self.fields['workitemtype'] = TreeNodeChoiceField(
        queryset=TYPE_HSDB.objects.filter(active=True, ),
        label='Select a Type',
        empty_label='--Select type --'
        )
        self.fields['workitemtype'].required = False
        self.fields['workitemtype'].empty_label = '--Select type--'        

        self.fields['parent'] = TreeNodeChoiceField(
            queryset=CORE_HSDB.objects.filter(active=True, ),
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
        model = CORE_HSDB
        fields = ['parent', 'title', 'workitemtype', 'description' , 'column', 'swimlane', 'done']


