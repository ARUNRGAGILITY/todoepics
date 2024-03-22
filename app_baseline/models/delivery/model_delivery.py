from ..all_model_imports import *
from ..type.model_type import *
from .model_coredelivery import *
from .model_typeprioritystate import *
# which app is being referred
# config
from ..._common.config.config import *
app_base_ref = base_app_ref


# inherited delivery models
# So far: Project/Product/Service/Solution/ValueStream/Organization

# Organization
class Organization(CoreDelivery):
    work_item_type = TreeForeignKey(f"{app_base_ref}.Type", on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_org_witype")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_org_author")
    def __str__(self):
        return self.title
    
class Project(CoreDelivery):
    # Additional fields specific to the Project model
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(BaseType, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(BaseState, null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.ForeignKey(BasePriority, null=True, blank=True, on_delete=models.SET_NULL)
    work_item_type = TreeForeignKey(f"{app_base_ref}.Type", on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_project_witype")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_project_author")


class Product(CoreDelivery):
    # Additional fields specific to the Product model
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(BaseType, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(BaseState, null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.ForeignKey(BasePriority, null=True, blank=True, on_delete=models.SET_NULL)
    work_item_type = TreeForeignKey(f"{app_base_ref}.Type", on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_product_witype")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_product_author")
  

class Service(CoreDelivery):
    # Additional fields specific to the Service model
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(BaseType, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(BaseState, null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.ForeignKey(BasePriority, null=True, blank=True, on_delete=models.SET_NULL)
    work_item_type = TreeForeignKey(f"{app_base_ref}.Type", on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_service_witype")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_service_author")
   

class Solution(CoreDelivery):
    # Additional fields specific to the Solution model
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(BaseType, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(BaseState, null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.ForeignKey(BasePriority, null=True, blank=True, on_delete=models.SET_NULL)
    work_item_type = TreeForeignKey(f"{app_base_ref}.Type", on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_solution_witype")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_solution_author")


class ValueStream(CoreDelivery):
    # Additional fields specific to the Solution model
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(BaseType, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(BaseState, null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.ForeignKey(BasePriority, null=True, blank=True, on_delete=models.SET_NULL)
    work_item_type = TreeForeignKey(f"{app_base_ref}.Type", on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_value_stream_witype")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_value_stream_author")
 

class Team(CoreDelivery):
    # Additional fields specific to the Solution model
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_team_author")
 
class Location(CoreDelivery):
    # Additional fields specific to the Solution model
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_location_author")

class Members(CoreDelivery):
    # Additional fields specific to the Solution model
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_member_author")

class VisionMissionValueSRI(CoreDelivery):
    # VMVSRI    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.SET_NULL)
    solution = models.ForeignKey(Solution, null=True, blank=True, on_delete=models.SET_NULL)
    valuestream = models.ForeignKey(ValueStream, null=True, blank=True, on_delete=models.SET_NULL)

    vision = MarkdownxField(null=True, blank=True)   
    test_field =  models.TextField(null=True, blank=True, default='')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_vmvsri_author")


class Board(CoreDelivery):
    # Board    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.SET_NULL)
    solution = models.ForeignKey(Solution, null=True, blank=True, on_delete=models.SET_NULL)
    valuestream = models.ForeignKey(ValueStream, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_board_author")
 

class Swimlane(CoreDelivery):
    # swimlane    (title and description will come from core delivery model)
    COLOR_CHOICES = (
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('grey', 'Grey'),
        ('orange', 'Orange'),
        ('purple', 'Purple'),
        ('yellow', 'Yellow'),
        ('brown', 'Brown'),
        # Add more color choices as needed
    )
    board = models.ForeignKey(Board, null=True, blank=True, on_delete=models.SET_NULL)   
    color =  models.CharField(max_length=100,null=True, blank=True, default='red', choices=COLOR_CHOICES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_swimlane_author")

   
class BoardSettings(CoreDelivery):
    # Board    Settings   
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_boardsettings_author")
    def __str__(self):
        return self.title

# models.py

class BoardColumns(CoreDelivery):
    board = models.ForeignKey(Board, null=True, blank=True, on_delete=models.SET_NULL)
    wip_limit = models.PositiveIntegerField(default=0,null=True, blank=True,)
    policies = models.TextField(null=True, blank=True, default='')
    entry_criteria = models.TextField(null=True, blank=True, default='')
    exit_criteria = models.TextField(null=True, blank=True, default='')
    cycle_time_column = models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_boardcolumns_author")
    def __str__(self):
        return self.title
  

class BoardBufferColumns(CoreDelivery):
    board_columns = models.ForeignKey(BoardColumns, null=True, blank=True, on_delete=models.SET_NULL)
    wip_limit = models.PositiveIntegerField(default=0,null=True, blank=True,)
    policies = models.TextField(null=True, blank=True, default='')
    entry_criteria = models.TextField(null=True, blank=True, default='')
    exit_criteria = models.TextField(null=True, blank=True, default='')
    cycle_time_column = models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_boardbuffercolumns_author")
    def __str__(self):
        return self.title


################################################################################################