from ..all_model_imports import *
from ..type.model_type import *

# which app is being referred
# config
from ..._common.config.config import *
app_base_ref = base_app_ref

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
  

    class Meta:
        ordering = ['position']
        abstract = True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todlist_home')
