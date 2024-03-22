# Base URL configuration for app_abc
from django.urls import path, include


# base view
from ...views.base import view_base
from ...views.user import view_user
from ...views.list import view_list 
# config
from ..._common.config.config import *
app_base_ref = f"{base_app_ref}"

urlpatterns_permission = [
    path('edit_permission/<int:permission_id>', view_list.edit_permission, name="edit_permission"),
    path('delete_permission/<int:permission_id>', view_list.delete_permission, name="delete_permission"),
    path('permission_settings/<int:list_id>', view_list.permission_settings, name="permission_settings"),
    path('ajax_user_suggest', view_list.ajax_user_suggest, name="ajax_user_suggest"),
]