from .all_imports import *
from .core_models import *
# dependency

### VSM ###
class VSM(models.Model):
    title =  models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True, default='')
    work_item_type = TreeForeignKey('app_xpresskanban.TYPE_HSDB', on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_vsm_witype")
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_vsm_author")

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todlist_home')

#### VSM related
class VSMS_Overview(models.Model):
    vsms = TreeForeignKey('app_xpresskanban.CORE_HSDB', on_delete=models.CASCADE, related_name='vsms_overview1')
    trigger =  models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True, default='')
    starting_point = models.TextField(null=True, blank=True, default='')
    end_point = models.TextField(null=True, blank=True, default='')
    demand_rate = models.TextField(null=True, blank=True, default='')
    boundaries_and_limitations = models.TextField(null=True, blank=True, default='')
    improvement_items = models.TextField(null=True, blank=True, default='')
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name="xpress_vsm_overview_author" )

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todlist_home')


#### VSM related
class VSMS_Info(models.Model):
    vsms = TreeForeignKey('app_xpresskanban.CORE_HSDB', on_delete=models.CASCADE, related_name='vsms_info1')
    title =  models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True, default='')

    total_value_time = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_non_value_time = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    end_to_end_time = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rolled_ca = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Add other fields for VSM metrics, such as cycle time, lead time, etc.
    organization_efficiency = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_vsm_info_author")

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todlist_home')

class VSMS_Steps(models.Model):
    #info = models.ForeignKey(VSMS_Info, null=True, blank=True, related_name='info_fk', on_delete=models.CASCADE)
    vsms = TreeForeignKey('app_xpresskanban.CORE_HSDB',  on_delete=models.CASCADE, related_name='vsms_steps1')
    title =  models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True, default='')

    role =  models.CharField(max_length=50, null=True, blank=True, default='')

    value_time = models.DecimalField(max_digits=10, decimal_places=2, default=0, )
    non_value_time = models.DecimalField(max_digits=10, decimal_places=2, default=0, )
    percentage_accurate = models.DecimalField(max_digits=10, decimal_places=2, default=1, )

    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_vsm_steps_author")

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todlist_home')
    