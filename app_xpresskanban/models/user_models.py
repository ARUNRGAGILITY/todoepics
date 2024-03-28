from .all_imports import *
from .core_models import *
from .delivery_models import * 

class UserPreference(models.Model):
    userid = models.CharField(max_length=50)
    scope =  models.CharField(max_length=256)
    setting =  models.CharField(max_length=256)
    preference =  models.CharField(max_length=256)    

    done = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_user_preference_author" )

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.userid

    def get_absolute_url(self):
        return reverse('todlist_home')
    
#
#
# Recently accessed boards
#
#
class RecentlyAccessedBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now=True)