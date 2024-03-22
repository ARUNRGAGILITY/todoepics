from ..all_model_imports import *
from ..type.model_type import *
from ..permission.model_permission import *
# which app is being referred
# config
from ..._common.config.config import *
app_base_ref = base_app_ref

class Work(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='CHILDREN', on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, default='', null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    # Type 
    type = TreeForeignKey(Type, null=True, blank=True, related_name='bltype', on_delete=models.CASCADE)
    # Administration
    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)
    done = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    # Management
    duration_in_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    class MPTTMeta:
        order_insertion_by = ['position']
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('list_home')
    def get_completion_stats(self):
        total_count = self.get_descendants().filter(done=True, active=True).count() + self.get_descendants().filter(done=False, active=True).count()
        completed_count = self.get_descendants().filter(done=True, active=True).count()
        percent_complete = round(completed_count / total_count * 100, 2) if total_count > 0 else 0.0
        logger.debug(f"====> {completed_count}/{total_count} ===> {percent_complete}")
        return {
            'total_count': total_count,
            'completed_count': completed_count,
            'percent_complete': percent_complete,
        }
    def get_active_descendants(self):
        return self.get_descendants().filter(active=True)
    def children(self):
        return Work.objects.filter(parent=self.pk, active=True)
    def serializable_object(self):
        obj = {'title': self.title, 'children': []}
        for child in self.children():
            obj['children'].append(child.serializable_object())
        return obj

