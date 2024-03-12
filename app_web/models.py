from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings  # Assuming your User model comes from settings.AUTH_USER_MODEL
from django.contrib.contenttypes.fields import GenericRelation

class OVS_Types(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ovstypes')

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

class DVS_Types(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='dvstypes')

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name


class OpsValueStream(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    trigger = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='authops')
   
    total_value_creation_time = models.IntegerField(default=0)
    total_delay_time = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)
    efficiency = models.FloatField(default=0.0)

    def update_efficiency(self):
        steps = self.steps.all()
        self.calculate_efficiency(steps)
        print(f">>> === {steps} testing update === <<<")
        self.save()

    def calculate_efficiency(self, steps):
        total_value_creation_time = sum(step.value_creation_time for step in steps)
        print(f">>> === {total_value_creation_time} testing calculate === <<<")
        total_delay_time = sum(step.delay_time for step in steps)
        total_time = total_value_creation_time + total_delay_time
        self.total_value_creation_time = total_value_creation_time
        self.total_delay_time = total_delay_time
        self.total_time = total_time
        # Avoid division by zero
        self.efficiency = (total_value_creation_time / total_time * 100) if total_time > 0 else 0
    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

class DevValueStream(models.Model):
    ops_valuestream = models.ForeignKey(OpsValueStream, null=True, blank=True, on_delete=models.SET_NULL, related_name='devvaluestream')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    supported_ops_steps = models.ManyToManyField('ValueStreamSteps', related_name='supporting_dev_streams', blank=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='authdev')

    
    total_value_creation_time = models.IntegerField(default=0)
    total_delay_time = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)
    efficiency = models.FloatField(default=0.0)

    def update_efficiency(self):
        steps = self.steps.all()
        self.calculate_efficiency(steps)
        print(f">>> === {steps} testing update === <<<")
        self.save()

    def calculate_efficiency(self, steps):
        total_value_creation_time = sum(step.value_creation_time for step in steps)
        print(f">>> === {total_value_creation_time} testing calculate === <<<")
        total_delay_time = sum(step.delay_time for step in steps)
        total_time = total_value_creation_time + total_delay_time
        self.total_value_creation_time = total_value_creation_time
        self.total_delay_time = total_delay_time
        self.total_time = total_time
        # Avoid division by zero
        self.efficiency = (total_value_creation_time / total_time * 100) if total_time > 0 else 0
    
    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name


# chotinikara bhavagathi ammae
class ValueStreamSteps(models.Model):
    opsvaluestream = models.ForeignKey(OpsValueStream, on_delete=models.CASCADE, related_name='steps', null=True, blank=True)
    devvaluestream = models.ForeignKey(DevValueStream, on_delete=models.CASCADE, related_name='steps', null=True, blank=True)

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    value_creation_time = models.IntegerField(default=0)
    delay_time = models.IntegerField(default=0)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='authsteps')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # After saving, update efficiency of the related value stream, if any
        if self.opsvaluestream:
            print(f">>> === SAVE ops === <<<")
            self.opsvaluestream.update_efficiency()
        elif self.devvaluestream:
            self.devvaluestream.update_efficiency()
        else:
            print(f">>> === NOT SAVING === <<<")

    def delete(self, *args, **kwargs):
        # Temporarily store the parent before deletion for efficiency update
        ops_parent = self.opsvaluestream
        dev_parent = self.devvaluestream
        super().delete(*args, **kwargs)
        # Update efficiency after deletion
        if ops_parent:
            ops_parent.update_efficiency()
            print(f">>> === {ops_parent} testing update === <<<")
        if dev_parent:
            dev_parent.update_efficiency()
    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    position = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='role')

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role, blank=True)  # Allow multiple roles
    bio = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    
    def __str__(self):
        return f'Profile of {self.user.username}'
    
    def save(self, *args, **kwargs):
        # Custom save logic here
        super(Profile, self).save(*args, **kwargs)  # Ensure this is called
