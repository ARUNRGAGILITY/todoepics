from django.db import models
from django.conf import settings

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role, blank=True)  # Allow multiple roles
    bio = models.TextField(blank=True,null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
    
    def save(self, *args, **kwargs):
        # Custom save logic here
        super(Profile, self).save(*args, **kwargs)  # Ensure this is called
