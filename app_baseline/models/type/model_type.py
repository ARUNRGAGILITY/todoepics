from ..all_model_imports import *
# refer to permission model in permission/model_permission.py 
class Type(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='CHILDREN', on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, default='', null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)

    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class MPTTMeta:
       order_insertion_by = ['position']

    def __str__(self):
        return f"{self.title}"
    def children(self):
        return Type.objects.filter(parent=self.pk, active=True)
    def get_active_descendants(self):
        return self.get_descendants().filter(active=True)
    def get_parent_id(self):
        if self.parent:
            return self.parent.id
        return None