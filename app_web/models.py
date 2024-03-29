from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings  # Assuming your User model comes from settings.AUTH_USER_MODEL
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField 
TreeForeignKey = models.ForeignKey

################# SAFe #####################
class BaseModel1(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['position']


##################################################################
# ORGANIZATION
##################################################################
class SAFeType(BaseModel1):
    docs = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
class Organization(BaseModel1):
    work_item_type = TreeForeignKey('app_xpresskanban.TYPE_HSDB', on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_org_witype1")
    org_type = models.ForeignKey(SAFeType, on_delete=models.CASCADE, related_name="organizations")

    def __str__(self):
        return self.name
##################################################################
# ORG ADMINS
##################################################################
class OrgAdmins(BaseModel1):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class ProjectAdmins(BaseModel1):
    # need to add projects
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
##################################################################
# STRATEGIC THEME
##################################################################
class StrategicTheme(BaseModel1):
    corresponding_mptt_id = models.ForeignKey('app_baseline.List', on_delete=models.CASCADE, default=1,
                                              related_name='app_web_strategic_themes', null=True, blank=True)
    def __str__(self):
        return self.name

class Objective(BaseModel1):
    #theme = models.ForeignKey(StrategicTheme, related_name='objectives', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class KeyResult(BaseModel1):
    objective = models.ForeignKey(Objective, related_name='key_results', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    target = models.TextField(null=True, blank=True)  # This can be adjusted based on the type of measurement.

    def __str__(self):
        return self.name

class QuarterlyMeasure(BaseModel1):
    key_result = models.ForeignKey(KeyResult, related_name='quarterly_measures', on_delete=models.CASCADE)
    quarter = models.CharField(max_length=2, choices=[('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3'), ('Q4', 'Q4')])
    year = models.PositiveIntegerField(null=True, blank=True)
    percentage = models.FloatField(null=True, blank=True)
    value = models.TextField(null=True, blank=True)  # This can be adjusted to match the type of metric you are measuring.

    def __str__(self):
        return f"{self.key_result.name} - {self.quarter} {self.year}"

# WBS

class TypeChoices(models.TextChoices):
    ENABLER = 'EN', _('Enabler')
    BUSINESS = 'BU', _('Business')
    
class Epic(BaseModel1):
    corresponding_mptt_id = models.ForeignKey('app_baseline.List', on_delete=models.CASCADE, 
                                              related_name='app_web_epics',null=True, blank=True)
    #strategictheme = models.ForeignKey(StrategicTheme, related_name='epics', on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TypeChoices.choices, default=TypeChoices.BUSINESS)

    def __str__(self):
        return self.name
    
    @classmethod
    def get_parent_model(cls):
        return 'StrategicTheme'
    
# Separate models for Feature and Capability
class Feature(BaseModel1):
    corresponding_mptt_id = models.ForeignKey('app_baseline.List', on_delete=models.CASCADE, 
                                              related_name='app_web_features', null=True, blank=True)
    #epic = models.ForeignKey(Epic, related_name='features', on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TypeChoices.choices, default=TypeChoices.BUSINESS)
    
    def __str__(self):
        return self.name
    
    @classmethod
    def get_parent_model(cls):
        return 'Epic'

class Capability(BaseModel1):
    corresponding_mptt_id = models.ForeignKey('app_baseline.List', on_delete=models.CASCADE, 
                                              related_name='app_web_capabilities', null=True, blank=True)
    #epic = models.ForeignKey(Epic, related_name='capabilities', on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TypeChoices.choices, default=TypeChoices.BUSINESS)

    def __str__(self):
        return self.name
    
    @classmethod
    def get_parent_model(cls):
        return 'Epic'

class Component(BaseModel1):
    corresponding_mptt_id = models.ForeignKey('app_baseline.List', on_delete=models.CASCADE, 
                                              related_name='app_web_components',null=True, blank=True)
    #epic = models.ForeignKey(Epic, related_name='components', on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TypeChoices.choices, default=TypeChoices.BUSINESS)

    def __str__(self):
        return self.name
    
    @classmethod
    def get_parent_model(cls):
        return 'Epic'
# Separate models for User Story and Spike
class UserStory(BaseModel1):
    corresponding_mptt_id = models.ForeignKey('app_baseline.List', on_delete=models.CASCADE, 
                                              related_name='app_web_user_stories', null=True, blank=True)
    #feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='user_stories', null=True, blank=True)
    #capability = models.ForeignKey(Capability, on_delete=models.CASCADE, related_name='user_stories', null=True, blank=True)
    #component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='user_stories', null=True, blank=True)
    # Additional fields specific to User Stories

    def save(self, *args, **kwargs):
        if self.parent_feature and self.parent_capability:
            raise ValueError("A User Story cannot be associated with both a Feature and a Capability.")
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

    @classmethod
    def get_parent_model(cls):
        return 'Feature/Capability/Component'
        
class Spike(BaseModel1):
    corresponding_mptt_id = models.ForeignKey('app_baseline.List', on_delete=models.CASCADE, 
                                              related_name='app_web_spikes', null=True, blank=True)
    #feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='spikes', null=True, blank=True)
    #capability = models.ForeignKey(Capability, on_delete=models.CASCADE, related_name='spikes', null=True, blank=True)
    #component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='spikes', null=True, blank=True)
    # Additional fields specific to Spikes
    
    def save(self, *args, **kwargs):
        if self.parent_feature and self.parent_capability:
            raise ValueError("A Spike cannot be associated with both a Feature and a Capability.")
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    @classmethod
    def get_parent_model(cls):
        return 'Feature/Capability/Component'

class Task(BaseModel1):
    # Assuming Tasks can belong to both User Stories and Spikes
    corresponding_mptt_id = models.ForeignKey('app_baseline.List', on_delete=models.CASCADE, 
                                              related_name='app_web_tasks',null=True, blank=True)
    #userstory = models.ForeignKey(UserStory, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    #spike = models.ForeignKey(Spike, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    # Additional fields specific to Tasks
    
    def __str__(self):
        return self.name

    @classmethod
    def get_parent_model(cls):
        return 'UserStory/Spike'

##################################################################
# VALUESTREAM
##################################################################

class DVS_Types(BaseModel1):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='dvstypes')

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name


class OpsValueStream(models.Model):
    name = models.CharField(max_length=255, unique=False)
    description = models.TextField(null=True, blank=True)
    trigger = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    owner = models.CharField(max_length=255, null=True, blank=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='authops')
   
    total_value_creation_time = models.IntegerField(default=0)
    total_delay_time = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)
    efficiency = models.FloatField(default=0.0)
    rolled_ca = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_efficiency(self):
        steps = self.steps.filter(active=True)
        self.calculate_efficiency(steps)
        self.calculate_rolled_ca(steps)  
        print(f">>> === |||||||==> count of steps {steps.count()} testing update === <<<")
        self.save()

    def calculate_rolled_ca(self, steps):
        if steps.exists():
            rolled_ca = 1
            for step in steps:
                rolled_ca *= step.percentage_accurate / 100
            self.rolled_ca = round(rolled_ca * 100, 2)  # Convert back to percentage
        else:
            self.rolled_ca = 0  # Reset to 0 if there are no steps

    def calculate_efficiency(self, steps):
        total_value_creation_time = sum(step.value_creation_time for step in steps)
        print(f">>> === {total_value_creation_time} testing calculate === <<<")
        total_delay_time = sum(step.delay_time for step in steps)
        total_time = total_value_creation_time + total_delay_time
        self.total_value_creation_time = total_value_creation_time
        self.total_delay_time = total_delay_time
        self.total_time = total_time
        # Avoid division by zero
        efficiency = (total_value_creation_time / total_time * 100) if total_time > 0 else 0
        self.efficiency = round(efficiency, 2)
    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

class DevValueStream(models.Model):
    ops_valuestream = models.ForeignKey(OpsValueStream, null=True, blank=True, 
                                        on_delete=models.SET_NULL, related_name='devvaluestream')
    name = models.CharField(max_length=255, unique=False)
    description = models.TextField(null=True, blank=True)
    trigger = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    owner = models.CharField(max_length=255, null=True, blank=True)
    supported_ops_steps = models.ManyToManyField('ValueStreamSteps', related_name='supporting_dev_streams', blank=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='authdev')

    
    total_value_creation_time = models.IntegerField(default=0)
    total_delay_time = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)
    efficiency = models.FloatField(default=0.0)
    rolled_ca = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_efficiency(self):
        steps = self.steps.filter(active=True)
        self.calculate_efficiency(steps)
        self.calculate_rolled_ca(steps)  
        print(f">>> === {steps} testing update === <<<")
        self.save()
        
    def calculate_rolled_ca(self, steps):
        if steps.exists():
            rolled_ca = 1
            for step in steps:
                rolled_ca *= step.percentage_accurate / 100
            self.rolled_ca = round(rolled_ca * 100, 2)  # Convert back to percentage
        else:
            self.rolled_ca = 0  # Reset to 0 if there are no steps

    def calculate_efficiency(self, steps):
        total_value_creation_time = sum(step.value_creation_time for step in steps)
        print(f">>> === {total_value_creation_time} testing calculate === <<<")
        total_delay_time = sum(step.delay_time for step in steps)
        total_time = total_value_creation_time + total_delay_time
        self.total_value_creation_time = total_value_creation_time
        self.total_delay_time = total_delay_time
        self.total_time = total_time
        # Avoid division by zero
        efficiency = (total_value_creation_time / total_time * 100) if total_time > 0 else 0
        self.efficiency = round(efficiency,2)
    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

##################################################################
# TRASNFORMATION CANVAS
##################################################################
class OpsTransformationCanvas(BaseModel1):
    opsvaluestream = models.ForeignKey(OpsValueStream, on_delete=models.CASCADE, related_name='ops_transformation_canvases')
    docs = models.TextField(null=True, blank=True)
    demand_rate = models.CharField(max_length=255, null=True, blank=True)
    boundaries_and_constraints = models.TextField(null=True, blank=True)
    improvement_items = models.TextField(null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                               null=True, blank=True, related_name='authopscanvas')
    def __str__(self):
        return f"Ops Transformation Canvas for {self.opsvaluestream.name}"

class DevTransformationCanvas(BaseModel1):
    devvaluestream = models.ForeignKey(DevValueStream, on_delete=models.CASCADE, related_name='dev_transformation_canvases')
    docs = models.TextField(null=True, blank=True)
    demand_rate = models.CharField(max_length=255, null=True, blank=True)
    boundaries_and_constraints = models.TextField(null=True, blank=True)
    improvement_items = models.TextField(null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                               null=True, blank=True, related_name='authdevcanvas')
    marked_steps_with_star = models.TextField(null=True, blank=True)
    marked_rows_with_tag = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Dev Transformation Canvas for {self.devvaluestream.name}"

class CurrentStateDTC(BaseModel1):
    dtc = models.ForeignKey(DevTransformationCanvas, on_delete=models.CASCADE, 
                            related_name='current_state_dtc')
    snapshot = JSONField(default=dict)
    def __str__(self):
        return f"CurrentState of DTC"

class FutureStateDTC(BaseModel1):
    dtc = models.ForeignKey(DevTransformationCanvas, on_delete=models.CASCADE, 
                            related_name='future_state_dtc')
    snapshot = JSONField(default=dict)
    def __str__(self):
        return f"FutureState of DTC"



# c b a
class ValueStreamSteps(models.Model):
    opsvaluestream = models.ForeignKey(OpsValueStream, on_delete=models.CASCADE, related_name='steps', null=True, blank=True)
    devvaluestream = models.ForeignKey(DevValueStream, on_delete=models.CASCADE, related_name='steps', null=True, blank=True)

    name = models.CharField(max_length=255, unique=False)
    description = models.TextField(null=True, blank=True)
    owner = models.CharField(max_length=255, null=True, blank=True)
    value_creation_time = models.IntegerField(default=0)
    delay_time = models.IntegerField(default=0)
    percentage_accurate = models.DecimalField(max_digits=10, decimal_places=2, default=1, )
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='authsteps')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # After saving, update efficiency of the related value stream, if any
        if self.opsvaluestream:
            print(f">>> === ****||||SAVE ops === <<<")
            self.opsvaluestream.update_efficiency()
        elif self.devvaluestream:
            print(f">>> === SAVE dev === <<<")
            self.devvaluestream.update_efficiency()
        else:
            print(f">>> === NOT SAVING === <<<")

    def delete(self, *args, **kwargs):
        # Temporarily store the parent before deletion for efficiency update
        ops_parent = self.opsvaluestream
        dev_parent = self.devvaluestream
        super().delete(*args, **kwargs)
        # Update efficiency after deletion
        if ops_parent:
            ops_parent.update_efficiency()
            print(f">>> === {ops_parent} testing update === <<<")
        if dev_parent:
            dev_parent.update_efficiency()
    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='role')

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

class AWProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organizations = models.ManyToManyField(Organization, related_name="members")
    roles = models.ManyToManyField(Role, blank=True)  # Allow multiple roles
    bio = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    
    def __str__(self):
        return f'Profile of {self.user.username}'
    
    def save(self, *args, **kwargs):
        # Custom save logic here
        super(AWProfile, self).save(*args, **kwargs)  # Ensure this is called


##################################################################
# end of model file
##################################################################

class OVS_Types(BaseModel1):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ovstypes')

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

##################################################################
# end of model file
##################################################################
from django.core.exceptions import ValidationError

class MappingWBS(BaseModel1):
    organization = models.OneToOneField('Organization', on_delete=models.CASCADE, unique=True)
    list = models.ForeignKey('app_baseline.List', on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        # Ensure that the list and type are related
        if self.list.type != self.type:
            raise ValidationError('The selected list must be of the specified type.')

    def __str__(self):
        return f"WBS Mapping for {self.organization.name}"

    class Meta:
        verbose_name = "WBS Mapping"
        verbose_name_plural = "WBS Mappings"
