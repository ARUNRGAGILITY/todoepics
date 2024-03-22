from ..all_model_imports import *
from ..type.model_type import *

# which app is being referred
# config
from ..._common.config.config import *
app_base_ref = base_app_ref

class BaseState(models.Model):
    title =  models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True, default='')
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="xpress_base_state1")

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
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name="xpress_base_priority1")

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
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name="xpress_base_type1")

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('typelist_home')