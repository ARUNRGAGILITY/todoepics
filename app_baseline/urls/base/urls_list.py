# Base URL configuration for app_abc
from django.urls import path, include


# base view
from ...views.base import view_base
from ...views.user import view_user
from ...views.list import view_list 
# config
from ..._common.config.config import *
app_base_ref = f"{base_app_ref}"

urlpatterns_list = [
    # list
    path('ajax_update_list_sorted', view_list.ajax_update_list_sorted, name='ajax_update_list_sorted'),
    path('ajax_update_list_item', view_list.ajax_update_list_item, name='ajax_update_list_item'),
    path('list_home', view_list.list_home, name='list_home'),
    path('edit_list/<int:list_id>', view_list.edit_list, name='edit_list'),
    path('delete_list_item/<int:list_id>', view_list.delete_list_item, name='delete_list_item'),

    # list items
    path('list_items/<int:list_id>', view_list.list_items, name='list_items'),
    path('clone_list_items/<int:list_id>', view_list.clone_list_items, name='clone_list_items'),
    path('deep_clone_list_items/<int:list_id>', view_list.deep_clone_list_items, name='deep_clone_list_items'),

    # experiment jstree
    path('ajax_clone_node', view_list.ajax_clone_node, name='ajax_clone_node'),
    path('ajax_copy_node', view_list.ajax_copy_node, name='ajax_copy_node'),
    path('ajax_delete_node', view_list.ajax_delete_node, name='ajax_delete_node'),
    path('ajax_update_list_item_description', view_list.ajax_update_list_item_description, name='ajax_update_list_item_description'),
    path('ajax_add_node', view_list.ajax_add_node, name='ajax_add_node'),
    path('ajax_move_node', view_list.ajax_move_node, name='ajax_move_node'),
    path('ajax_rename_list_item', view_list.ajax_rename_list_item, name='ajax_rename_list_item'),
    path('ajax_get_node_details', view_list.ajax_get_node_details, name='ajax_get_node_details'),
    path('ajax_get_node_details_template', view_list.ajax_get_node_details_template, name='ajax_get_node_details_template'),
    path('ajax_get_tree_data', view_list.ajax_get_tree_data, name='ajax_get_tree_data'),
    path('ajax_get_tree_data_id', view_list.ajax_get_tree_data_id, name='ajax_get_tree_data_id'),
    path('list_js_tree', view_list.list_js_tree, name='list_js_tree'),
    path('list_js_tree_id/<int:list_id>', view_list.list_js_tree_id, name='list_js_tree_id'),
    path('ajax_get_type_details', view_list.ajax_get_type_details, name='ajax_get_type_details'),
    path('ajax_get_settings', view_list.ajax_get_settings, name='ajax_get_settings'),
    path('ajax_save_list_permission', view_list.ajax_save_list_permission, name='ajax_save_list_permission'),

    path('test_method/<int:list_id>', view_list.test_method, name='test_method'),
    path('ajax_update_tree_field', view_list.ajax_update_tree_field, name='ajax_update_tree_field'),
    
]
