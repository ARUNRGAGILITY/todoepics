from ..all_model_imports import *
from ..type.model_type import *
from ..delivery.model_coredelivery import *
# Organization
class UserVisited(CoreDelivery):
    path_visited = models.TextField(null=True, blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name=f"{app_base_ref}_ua_author")
    def __str__(self):
        return self.title
    