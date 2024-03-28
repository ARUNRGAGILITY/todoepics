from .all_imports import *
from .core_models import *

# Declaring Base - State, Priority, Type
# Inherting by Project, Product, Service, Solution, ValueStream
class BaseState(models.Model):
    title =  models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True, default='')
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name="xpress_base_state")

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('typelist_home')

class BasePriority(models.Model):
    title =  models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True, default='')
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_base_priority")

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('typelist_home')

class BaseType(models.Model):
    title =  models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True, default='')
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_base_type")

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('typelist_home')


# General Objects details
# Delivery Models for Project,Product, Service, Solution, ValueStream
class GeneralObject(models.Model):
    done = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    

    class Meta:
        ordering = ['position']
        abstract = True


# Delivery Models for Project,Product, Service, Solution, ValueStream
class CoreDelivery(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True, default='')    

    start_date = models.DateField(null=True, blank=True, default=None)
    end_date = models.DateField(null=True, blank=True, default=None)
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)

    progress = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    current_state = models.TextField(null=True, blank=True, default='')

    done = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    duration_in_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)
    
    # # m2m fields 
    # # Define viewers, editors, and admins fields here
    # viewers = models.ManyToManyField(User, related_name='viewable_%(class)s', blank=True)
    # editors = models.ManyToManyField(User, related_name='editable_%(class)s', blank=True)
    # admins = models.ManyToManyField(User, related_name='admin_%(class)s', blank=True)


    class Meta:
        ordering = ['position']
        abstract = True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todlist_home')

# inherited delivery models
# So far: Project/Product/Service/Solution/ValueStream/Organization

# Organization
class Organization(CoreDelivery):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_org_author")
    def __str__(self):
        return self.title
    
class Project(CoreDelivery):
    # Additional fields specific to the Project model
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(BaseType, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(BaseState, null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.ForeignKey(BasePriority, null=True, blank=True, on_delete=models.SET_NULL)
    work_item_type = TreeForeignKey('app_xpresskanban.TYPE_HSDB', on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_project_witype")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_project_author")

     # m2m fields 
    # Define viewers, editors, and admins fields here
    viewers = models.ManyToManyField(User, related_name='viewable_projects', blank=True)
    editors = models.ManyToManyField(User, related_name='editable_projects', blank=True)
    admins = models.ManyToManyField(User, related_name='admin_projects', blank=True)



    class Meta:
        permissions = [
            ("can_view_project", "Can view Project"),
            ("can_edit_project", "Can edit Project"),
            ("can_admin_project", "Can admin Project"),
        ]

class Product(CoreDelivery):
    # Additional fields specific to the Product model
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(BaseType, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(BaseState, null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.ForeignKey(BasePriority, null=True, blank=True, on_delete=models.SET_NULL)
    work_item_type = TreeForeignKey('app_xpresskanban.TYPE_HSDB', on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_product_witype")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_product_author")

    class Meta:
        permissions = [
            ("can_view_product", "Can view Product"),
            ("can_edit_product", "Can edit Product"),
            ("can_admin_product", "Can admin Product"),
        ]

class Service(CoreDelivery):
    # Additional fields specific to the Service model
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(BaseType, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(BaseState, null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.ForeignKey(BasePriority, null=True, blank=True, on_delete=models.SET_NULL)
    work_item_type = TreeForeignKey('app_xpresskanban.TYPE_HSDB', on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_service_witype")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_service_author")

    class Meta:
        permissions = [
            ("can_view_service", "Can view Service"),
            ("can_edit_service", "Can edit Service"),
            ("can_admin_service", "Can admin Service"),
        ]

class Solution(CoreDelivery):
    # Additional fields specific to the Solution model
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(BaseType, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(BaseState, null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.ForeignKey(BasePriority, null=True, blank=True, on_delete=models.SET_NULL)
    work_item_type = TreeForeignKey('app_xpresskanban.TYPE_HSDB', on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_solution_witype")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_solution_author")

    class Meta:
        permissions = [
            ("can_view_solution", "Can view Solution"),
            ("can_edit_solution", "Can edit Solution"),
            ("can_admin_solution", "Can admin Solution"),
        ]


class ValueStream(CoreDelivery):
    # Additional fields specific to the Solution model
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(BaseType, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(BaseState, null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.ForeignKey(BasePriority, null=True, blank=True, on_delete=models.SET_NULL)
    work_item_type = TreeForeignKey('app_xpresskanban.TYPE_HSDB', on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_value_stream_witype")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_value_stream_author")

    class Meta:
        permissions = [
            ("can_view_valuestream", "Can view ValueStream"),
            ("can_edit_valuestream", "Can edit ValueStream"),
            ("can_admin_valuestream", "Can admin ValueStream"),
        ]


class Team(CoreDelivery):
    # Additional fields specific to the Solution model
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_team_author")

    class Meta:
        permissions = [
            ("can_view_team", "Can view Team"),
            ("can_edit_team", "Can edit Team"),
            ("can_admin_team", "Can admin Team"),
        ]

class Members(CoreDelivery):
    # Additional fields specific to the Solution model
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_member_author")


from markdownx.models import MarkdownxField
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

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_vmvsri_author")


class Board(CoreDelivery):
    # Board    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    organization =  models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.SET_NULL)
    solution = models.ForeignKey(Solution, null=True, blank=True, on_delete=models.SET_NULL)
    valuestream = models.ForeignKey(ValueStream, null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_board_author")

    class Meta:
        permissions = [
            ("can_view_board", "Can view Board"),
            ("can_edit_board", "Can edit Board"),
            ("can_admin_board", "Can admin Board"),
        ]

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
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_swimlane_author")

    class Meta:
        permissions = [
            ("can_view_swimlane", "Can view Swimlane"),
            ("can_edit_swimlane", "Can edit Swimlane"),
            ("can_admin_swimlane", "Can admin Swimlane"),
        ]
class BoardSettings(CoreDelivery):
    # Board    Settings   
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_boardsettings_author")
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
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_boardcolumns_author")
    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [
            ("can_view_boardcolumns", "Can view BoardColumns"),
            ("can_edit_boardcolumns", "Can edit BoardColumns"),
            ("can_admin_boardcolumns", "Can admin BoardColumns"),
        ]

class BoardBufferColumns(CoreDelivery):
    board_columns = models.ForeignKey(BoardColumns, null=True, blank=True, on_delete=models.SET_NULL)
    wip_limit = models.PositiveIntegerField(default=0,null=True, blank=True,)
    policies = models.TextField(null=True, blank=True, default='')
    entry_criteria = models.TextField(null=True, blank=True, default='')
    exit_criteria = models.TextField(null=True, blank=True, default='')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_boardbuffercolumns_author")
    def __str__(self):
        return self.title


class BoardHistory(CoreDelivery):
    board = models.ForeignKey(Board, null=True, blank=True, on_delete=models.SET_NULL)
    card_id = TreeForeignKey('app_xpresskanban.CORE_HSDB', on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_board_history")
    src_column_id = models.ForeignKey(BoardColumns, null=True, blank=True, on_delete=models.SET_NULL, related_name="src_column")
    dest_column_id = models.ForeignKey(BoardColumns, null=True, blank=True, on_delete=models.SET_NULL, related_name="dest_column")
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_board_history_changedby")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_board_history_author")
    def __str__(self):
        return self.title



# SUPER IMPORTANT 
# def board_view(request, project_id, board_id):
#     project = Project.objects.get(id=project_id)
#     board = Board.objects.get(id=board_id, project=project)
#     tasks = Task.objects.filter(swimlane__board=board)

#     context = {
#         'project': project,
#         'board': board,
#         'tasks': tasks,
#     }

#     return render(request, 'board_template.html', context)



# Release 
class Release(GeneralObject):
    RELEASE_REQUEST = (
        ('OD', 'On-Demand'),
        ('SC', 'Scheduled'),
    )
    RELEASE_TYPE = (
        ('Major', 'Major'),
        ('Minor', 'Minor'),
        ('Patch', 'Patch'),
        ('Hot-Fix', 'Hot-Fix'),
        ('Service-Pack', 'Service-Pack'),
    )
    
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=100,null=True, blank=True,)
    market_name = models.CharField(max_length=100,null=True, blank=True,)
    release_request = models.CharField(max_length=2, choices=RELEASE_REQUEST,null=True, blank=True,)
    release_type = models.CharField(max_length=40, choices=RELEASE_TYPE,null=True, blank=True,)
    release_date = models.DateField(null=True, blank=True,)
    def __str__(self):
        return self.name
    
class Sprint(GeneralObject):
    SPRINT_TYPES = (
        ('I', 'Iteration'),
        ('S', 'Sprint'),
    )
    sprint_type = models.CharField(max_length=1, choices=SPRINT_TYPES)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    release = models.ForeignKey(Release, on_delete=models.CASCADE)  
    
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True,)
    goal = models.TextField(null=True, blank=True,)

    sprint_no = models.PositiveIntegerField(null=True, blank=True,default=0)

    start_date = models.DateField(null=True, blank=True,)
    end_date = models.DateField(null=True, blank=True,)
    
    total_person_hours = models.IntegerField(null=True, blank=True, default=0)
    no_of_days = models.IntegerField(null=True, blank=True, default=0)


    def __str__(self):
        sprint_type_display = dict(Sprint.SPRINT_TYPES)[self.sprint_type]
        return f"{sprint_type_display} {self.sprint_no} ({self.release})"

    @classmethod
    def create_sprints(cls, project, no_of_sprints, start_date, sprint_duration_weeks=2):
        sprints = []
        for i in range(no_of_sprints):
            sprint_name = f"Sprint {i + 1}"
            end_date = start_date + timedelta(weeks=sprint_duration_weeks) - timedelta(days=1)
            sprint = cls(
                project=project,
                sprint_name=sprint_name,
                sprint_no=i + 1,
                start_date=start_date,
                end_date=end_date,
                release="",
                goal="",
                description="",
            )
            sprints.append(sprint)
            start_date = end_date + timedelta(days=1)
        cls.objects.bulk_create(sprints)


class SprintTask(GeneralObject):
    sprint = models.ForeignKey(Sprint,null=True, blank=True, on_delete=models.SET_NULL) 
    sprint_task = models.TextField(null=True, blank=True,)
    initial_estimate = models.IntegerField(null=True, blank=True, default=0)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_sprint_task")
class SprintTaskDays(GeneralObject):
    sprint_task = models.ForeignKey(SprintTask,null=True, blank=True, on_delete=models.SET_NULL)    
    day = models.IntegerField(null=True, blank=True, default=0)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_sprint_day")
class SprintDayTotalHours(GeneralObject):
    sprint = models.ForeignKey(Sprint,null=True, blank=True, on_delete=models.SET_NULL) 
    day = models.IntegerField(null=True, blank=True, default=0)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_sprint_dayhours")
