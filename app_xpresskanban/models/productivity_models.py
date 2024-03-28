from .all_imports import *

class Planner(models.Model):
    title =  models.CharField(max_length=256)
    who = models.CharField(max_length=100,null=True, blank=True, default='')
    description = models.TextField(null=True, blank=True, default='')  
    done = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_in_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_planner")

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todlist_home')