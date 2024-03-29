from ..all_model_imports import *



# SSRT 

# Core Models
class TYPE_HSDB(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='TYPELIST', on_delete=models.CASCADE)
    title =  models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True, default='')
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='TL_TLIST')

    class MPTTMeta:
        order_insertion_by = ['position']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('typelist_home')
    
    def get_active_descendants(self):
        return self.get_descendants().filter(active=True)
    def get_parent_id(self):
        if self.parent:
            return self.parent.id
        return None

    ## display 
    def children(self):
        return TYPE_HSDB.objects.filter(parent=self.pk, active=True)
    def serializable_object(self):
        obj = {'title': self.title, 'children': []}
        for child in self.children():
            obj['children'].append(child.serializable_object())
        return obj

# Core Hierarchical System Database
class CORE_HSDB(MPTTModel):
    service = models.ForeignKey('app_baseline.Service', on_delete=models.CASCADE, related_name='backlogs', null=True, blank=True)
    solution = models.ForeignKey('app_baseline.Solution', on_delete=models.CASCADE, related_name='product_backlog', null=True, blank=True)
    project = models.ForeignKey('app_baseline.Project', on_delete=models.CASCADE, related_name='backlogs', null=True, blank=True)
    product = models.ForeignKey('app_baseline.Product', on_delete=models.CASCADE, related_name='product_backlog', null=True, blank=True)
    value_stream = models.ForeignKey('app_baseline.ValueStream', on_delete=models.CASCADE, related_name='vsm_vs', null=True, blank=True)
    
    # mapping
    #vsm = models.ForeignKey('app_baseline.VSM', on_delete=models.CASCADE, related_name='vsm_vs', null=True, blank=True)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='CHILDREN', on_delete=models.CASCADE)
    title =  models.CharField(max_length=256)
    workitemtype = TreeForeignKey(TYPE_HSDB, null=True, blank=True, related_name='CH_WITYPE', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True, default='')
    done = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_in_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    active = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='CORE_HSDB_TODOLIST')

    class MPTTMeta:
        order_insertion_by = ['position']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todlist_home')

    def get_completion_stats(self):
        total_count = self.get_descendants().filter(done=True, active=True).count() + self.get_descendants().filter(done=False, active=True).count()
        completed_count = self.get_descendants().filter(done=True, active=True).count()
        percent_complete = round((completed_count / total_count) * 100, 2) if total_count > 0 else 0.0
        #print(f"====> {completed_count}/{total_count} ===> {percent_complete}")
        return {
            'total_count': total_count,
            'completed_count': completed_count,
            'percent_complete': percent_complete,
        }
    
    def get_active_descendants(self):
        return self.get_descendants().filter(active=True)

    ## display 
    def children(self):
        return CORE_HSDB.objects.filter(parent=self.pk, active=True)
    def serializable_object(self):
        obj = {'title': self.title, 'children': []}
        for child in self.children():
            obj['children'].append(child.serializable_object())
        return obj
    
