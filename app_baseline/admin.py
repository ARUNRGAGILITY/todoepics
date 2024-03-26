from django.contrib import admin
from .models.user.model_user import *
from .models.list.model_list import *
from .models.admin.model_useranalytics import *
from .models.permission.model_permission import *
# TypeType
class TypeTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description' ,'active', 'deleted')
admin.site.register(TypeType, TypeTypeAdmin)

# List
class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'title', 'description' ,'type', 'user','active', 'done')
admin.site.register(List, ListAdmin)

admin.site.register(Profile)
admin.site.register(RegCode)
admin.site.register(CustomGroup)

# User Analytics
class UserVisitedAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description' ,'user', 'path_visited', 'created_at')
admin.site.register(UserVisited, UserVisitedAdmin)


class ListPermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'active', 'list_node',  'inherit', 'users_can_view', 'can_view', 'can_add', 'can_change', 'can_delete')
admin.site.register(ListPermission, ListPermissionAdmin)