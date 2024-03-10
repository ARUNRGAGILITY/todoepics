from django.db import models
from django.conf import settings
# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(blank=True)
    # Add other fields as needed

    def __str__(self):
        return f'Profile of {self.user.username}'
