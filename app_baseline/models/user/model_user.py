# import
from ..all_model_imports import *

  
class Role(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)

    start_date = models.DateField(null=True, blank=True, default=None)
    end_date = models.DateField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(null=True, blank=True)

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"
  

class RegCode(models.Model):
    reg_code = models.CharField(max_length=250, default='a1A1B1B2C1C3N4', null=False, blank=False)
    
    def __str__(self):
        return str(self.reg_code)
    

class CustomGroup(Group):    
    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="custom_group_user")

    def __str__(self):
        return self.name
