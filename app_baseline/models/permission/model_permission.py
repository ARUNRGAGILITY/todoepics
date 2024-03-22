from ..all_model_imports import *
from ...models.user.model_user import *
from ...models.list.model_list import *

from ..._common.config.config import *
app_base_ref = base_app_ref


class ListPermission(models.Model):
    list_node = TreeForeignKey(f"{app_base_ref}.List", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    # other fields like can_view, can_edit, etc.
    inherit = models.BooleanField(default=False)
    
    users_can_view = models.BooleanField(default=False) # can set for generally viewable elements

    can_view = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)
    can_change = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.can_delete:
            self.can_view = self.can_add = self.can_change = True
        elif self.can_change:
            self.can_view = self.can_add = True
        elif self.can_add:
            self.can_view = True
        super(ListPermission, self).save(*args, **kwargs)

