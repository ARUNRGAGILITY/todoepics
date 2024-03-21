from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import *
from django.contrib import admin
from django.apps import apps

# canvas
class OpsTransformationCanvasAdmin(admin.ModelAdmin):
    list_display = ('opsvaluestream', 'name', 'description', 'active', 'deleted') 
admin.site.register(OpsTransformationCanvas, OpsTransformationCanvasAdmin)
class DevTransformationCanvasAdmin(admin.ModelAdmin):
    list_display = ('devvaluestream', 'name', 'description', 'marked_steps_with_star', 'marked_rows_with_tag', 'active', 'deleted') 
admin.site.register(DevTransformationCanvas, DevTransformationCanvasAdmin)


# organizations
admin.site.register(SAFeType)
#admin.site.register(Organization)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_organizations')  # Example display columns
    filter_horizontal = ('organizations',)  # This makes it easier to edit many-to-many relationships

    def get_organizations(self, obj):
        return ", ".join([organization.name for organization in obj.organizations.all()])
    get_organizations.short_description = 'Organizations'
admin.site.register(Profile, ProfileAdmin)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'safe_type', 'active', 'deleted', )
admin.site.register(Organization, OrganizationAdmin)
## cafe

admin.site.register(Objective)
admin.site.register(KeyResult)
admin.site.register(QuarterlyMeasure)
# wbs
admin.site.register(Epic)
admin.site.register(Feature)
admin.site.register(Capability)
admin.site.register(Spike)

# class ProfileAdmin(admin.ModelAdmin):
#     filter_horizontal = ('organizations',) # Enables a user-friendly widget for managing many-to-many relationships

# admin.site.register(Profile, ProfileAdmin)

class ValueStreamStepsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner', 'active', 'deleted', )
    # Add any other fields you want to display in the admin list view

# Register the model and ModelAdmin with the admin site
admin.site.register(ValueStreamSteps, ValueStreamStepsAdmin)

class EpicInline(admin.TabularInline):  # You can also use admin.StackedInline for a different layout
    model = Epic
    extra = 1  # Specifies the number of blank forms to display by default
@admin.register(StrategicTheme)
class StrategicThemeAdmin(admin.ModelAdmin):
    inlines = [EpicInline]

class TaskInline(admin.TabularInline):  # You can also use admin.StackedInline for a different layout
    model = Task
    extra = 1  # Specifies the number of blank forms to display by default
    fk_name = 'parent_story'  # This is n
    
@admin.register(UserStory)
class UserStoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']  # Customize as needed
    inlines = [TaskInline]

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'parent_story', 'parent_spike',)
    list_filter = ('parent_story', 'parent_spike', )
    search_fields = ('name', 'description')

admin.site.register(Task, TaskAdmin)
## cafe


admin.site.register(Role)
admin.site.register(OpsValueStream)
admin.site.register(DevValueStream)
#admin.site.register(ValueStreamSteps)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_select_related = ('profile', )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
