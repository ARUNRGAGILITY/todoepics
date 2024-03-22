# Base URL configuration for app_abc
from django.urls import path, include


# base view
from ...views.base import view_base
from ...views.user import view_user
from ...views.list import view_list 
from ...views.type import view_type
# config
from ..._common.config.config import *
app_base_ref = f"{base_app_ref}"

urlpatterns_type = [
    # type
    path('type_home', view_type.type_home, name='type_home'),
    path('type_items/<int:type_id>', view_type.type_items, name='type_items'),
    path('ajax_update_type_sorted', view_type.ajax_update_type_sorted, name='ajax_update_type_sorted'),
    path('ajax_update_type_item', view_type.ajax_update_type_item, name='ajax_update_type_item'),    
    path('delete_type_item/<int:type_id>', view_type.delete_type_item, name='delete_type_item'),

    # type items    
    path('clone_type_items/<int:type_id>', view_type.clone_type_items, name='clone_type_items'),
    path('deep_clone_type_items/<int:type_id>', view_type.deep_clone_type_items, name='deep_clone_type_items'),

    # experiment jstree
    path('ajax_type_add_node', view_type.ajax_type_add_node, name='ajax_type_add_node'),
    path('ajax_type_move_node', view_type.ajax_type_move_node, name='ajax_type_move_node'),
    path('ajax_rename_type_item', view_type.ajax_rename_type_item, name='ajax_rename_type_item'),
    path('ajax_type_get_node_details/<int:type_id>', view_type.ajax_type_get_node_details, name='ajax_type_get_node_details'),
    path('ajax_type_get_tree_data', view_type.ajax_type_get_tree_data, name='ajax_type_get_tree_data'),
    path('ajax_type_get_tree_data_id', view_type.ajax_type_get_tree_data_id, name='ajax_type_get_tree_data_id'),
    path('type_js_tree', view_type.type_js_tree, name='type_js_tree'),
    path('type_js_tree_id/<int:type_id>', view_type.type_js_tree_id, name='type_js_tree_id'),
    path('ajax_type_clone_node', view_type.ajax_type_clone_node, name='ajax_type_clone_node'),
    path('ajax_type_copy_node', view_type.ajax_type_copy_node, name='ajax_type_copy_node'),
    path('ajax_type_delete_node', view_type.ajax_type_delete_node, name='ajax_type_delete_node'),
    path('ajax_update_type_item_description', view_type.ajax_update_type_item_description, name='ajax_update_type_item_description'),
    
]
