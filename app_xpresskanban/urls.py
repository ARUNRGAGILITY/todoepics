from django.urls import path, include
from app_xpresskanban.views.general import *
from app_xpresskanban.views.create_value import *
from app_xpresskanban.views.backlog import *
from app_xpresskanban.views.kanban_boards import *
from app_xpresskanban.views.cards_view import *
from app_xpresskanban.views.board_metrics_view import *
from app_xpresskanban.views.view_user_group_team_mgmt import *
from app_xpresskanban.views.view_board_settings import *
from app_xpresskanban.views.views_kanban_home import *
from app_xpresskanban.views.view_value_settings import *
from app_xpresskanban.views.view_user_pref import *
urlpatterns = [
    path('', kanban_home, name="kanban_home"),
    # Kanban related links
    ## Learn Kanban
    path('', kanban_home, name="home"),
    path('learn_kanban', learn_kanban, name="learn_kanban"),
    path('implement_kanban', implement_kanban, name="implement_kanban"),
    path('teach_kanban', teach_kanban, name="teach_kanban"),

    # General CRUD
    path('add_object/<str:model_name>', add_object, name="add_object"),
    path('create_value/<str:value_type>', create_value, name="create_value"),
    path('list_values/<str:value_type>', list_values, name="list_values"),
    path('value_homepage/<str:value_type>/<int:pk>', value_homepage, name="value_homepage"),
    path('bulk_restore_deleted_values/<str:value_type>', bulk_restore_deleted_values, name="bulk_restore_deleted_values"),
    path('copy_value/<str:value_type>/<int:pk>', copy_value, name="copy_value"),
    path('restore_value/<str:value_type>/<int:pk>', restore_value, name="restore_value"),
    path('restore_values/<str:value_type>', restore_values, name="restore_values"),
    path('ops_value/<str:value_type>', ops_value, name="ops_value"),
    path('view_value/<str:value_type>/<int:pk>', view_value, name="view_value"),
    path('edit_value/<str:value_type>/<int:pk>', edit_value, name="edit_value"),
    path('delete_value/<str:value_type>/<int:pk>', delete_value, name="delete_value"),
    path('sorted/<str:value_type>', sorted_value, name="sorted_value"),
    path('value_settings/<str:value_type>/<int:pk>', value_settings_main, name="value_settings"),
    path('val_remove_user_from_group/<str:value_type>/<int:pk>', val_remove_user_from_group, name="val_remove_user_from_group"),

    # backlog: this will get the PPSSVS id and send to backlog_home to fetch CORE_HSDB
    path('backlog_home/<str:value_type>/<int:pk>', backlog_home, name="backlog_home"),

    # board
    path('create_board/<str:value_type>/<int:pk>', create_board, name="create_board"),
    path('boards_home/<str:value_type>/<int:pk>', boards_home, name="boards_home"),
    path('ops_board/<str:value_type>/<int:board_id>', ops_board, name="ops_board"),
    path('sorted_boards/<str:value_type>/<int:pk>', sorted_boards, name="sorted_boards"),
    path('kanban_board/<str:value_type>/<int:pk>/<int:board_id>', kanban_board, name="kanban_board"),
    path('restore_an_item/<str:value_type>/<int:pk>/<int:board_id>', restore_an_item, name="restore_an_item"),
    path('bulk_restore_deleted_items/<str:value_type>/<int:pk>', bulk_restore_deleted_items, name="bulk_restore_deleted_items"),
    path('copy_value/<str:value_type>/<int:pk>', copy_value, name="copy_value"),
    path('list_deleted_items/<str:value_type>/<int:pk>', list_deleted_items, name="list_deleted_items"),
    path('edit_item/<str:value_type>/<int:pk>/<int:board_id>', edit_item, name="edit_item"),
    path('view_item/<str:value_type>/<int:pk>/<int:board_id>', view_item, name="view_item"),
    path('delete_item/<str:value_type>/<int:pk>/<int:board_id>', delete_item, name="delete_item"),
    path('board_settings/<str:value_type>/<int:pk>/<int:board_id>', board_settings_main, name="board_settings"),
    path('remove_user_from_group/<str:value_type>/<int:pk>/<int:board_id>', remove_user_from_group, name="remove_user_from_group"),
    # table view
    path('restore_show_deleted_cards/<str:value_type>/<int:pk>/<int:board_id>', restore_show_deleted_cards, name="restore_show_deleted_cards"),

    # view table
    path('table_view/<str:value_type>/<int:pk>/<int:board_id>', table_view, name="table_view"),
    path('ops_kanban/<str:value_type>/<int:pk>/<int:board_id>', ops_kanban, name="ops_kanban"),
    # charter
    path('create_charter/<str:value_type>/<int:pk>', create_charter, name="create_charter"),
    # card
    path('edit_card/<str:value_type>/<int:pk>/<int:board_id>/<int:card_id>', edit_card, name="edit_card"),
    path('view_card/<str:value_type>/<int:pk>/<int:board_id>/<int:card_id>', view_card, name="view_card"),
    path('delete_card/<str:value_type>/<int:pk>/<int:board_id>/<int:card_id>', delete_card, name="delete_card"),
    path('copy_card/<str:value_type>/<int:pk>/<int:board_id>/<int:card_id>', edit_card, name="copy_card"),
    path('clone_card/<str:value_type>/<int:pk>/<int:board_id>/<int:card_id>', edit_card, name="clone_card"),
    path('ajaxupdate_card', ajaxupdate_card, name="ajaxupdate_card"),
    path('bulk_restore_deleted_cards/<str:value_type>/<int:pk>/<int:board_id>', bulk_restore_deleted_cards, name="bulk_restore_deleted_cards"),
    # board columns
    path('kanban_board_columns/<str:value_type>/<int:pk>/<int:board_id>', kanban_board_columns, name="kanban_board_columns"),
    path('edit_column/<str:value_type>/<int:pk>/<int:board_id>/<int:column_id>', edit_column, name="edit_column"),
    path('delete_column/<str:value_type>/<int:pk>/<int:board_id>/<int:column_id>', delete_column, name="delete_column"),
    path('sorted_board_columns/<str:value_type>/<int:pk>/<int:board_id>', sorted_board_columns, name="sorted_board_columns"),
    path('update_task_column/<int:task_id>/<int:column_id>', update_task_column, name="update_task_column"),
    path('ajaxupdate_task_column', ajaxupdate_task_column, name="ajaxupdate_task_column"),
    path('ajax_board_updated', ajax_board_updated, name="ajax_board_updated"),
    path('ajax_sorted_kanban_board', ajax_sorted_kanban_board, name="ajax_sorted_kanban_board"),
    path('board_metrics/<int:board_id>', board_metrics, name="board_metrics"),
    path('ajaxupdate_column', ajaxupdate_column, name="ajaxupdate_column"),
    # swimlanes
    path('kanban_swimlanes/<str:value_type>/<int:pk>/<int:board_id>', kanban_swimlanes, name="kanban_swimlanes"),
    path('edit_swimlane/<str:value_type>/<int:pk>/<int:board_id>/<int:sl_id>', edit_swimlane, name="edit_swimlane"),
    path('delete_swimlane/<str:value_type>/<int:pk>/<int:board_id>/<int:sl_id>', delete_swimlane, name="delete_swimlane"),
    path('sorted_swimlanes/<str:value_type>/<int:pk>/<int:board_id>', sorted_swimlanes, name="sorted_swimlanes"),
    # PLACE HOLDER
    path('manage_value/<str:value_type>/<int:pk>', manage_value, name="manage_value"),

    # MANAGEMENT
    # User/Group
    path('user_group_mgmt_home', user_group_mgmt_home, name="user_group_mgmt_home"),

    # Board Settings 
    path('board_settings/<str:value_type>/<int:pk>/<int:board_id>', board_settings, name="board_settings"),
    
    
    ## GOALS ##
     path('', main_home, name='main_home'),
    # User Mgmt
    path('usermgmt/home/', user_home, name='user_mgmt_home'),
    path('usermgmt/list/', user_list, name='user_mgmt_list'),
    path('usermgmt/restore-deleted-user-list/', restore_user_list, name='user_mgmt_restore'),
    path('usermgmt/create/', user_create, name='user_mgmt_create'),
    path('usermgmt/create-multiple/', user_create_multiple, name='user_mgmt_create_multiple'),
    path('usermgmt/<int:pk>/', user_detail, name='user_mgmt_detail'),
    path('usermgmt/<int:pk>/update/', user_update, name='user_mgmt_update'),
    path('usermgmt/<int:pk>/delete/', user_delete, name='user_mgmt_delete'),
    path('ops_user_mgmt', ops_user_mgmt, name='ops_user_mgmt'),
    path('bulk_ops_user_mgmt', bulk_ops_user_mgmt, name='bulk_ops_user_mgmt'),
    # Group
    path('groupmgmt/home/', group_home, name='group_mgmt_home'),
    path('groupmgmt/list/', group_list, name='group_mgmt_list'),
    path('groupmgmt/create/', group_create, name='group_mgmt_create'),
    path('groupmgmt/<int:pk>/update/', group_update, name='group_mgmt_update'),
    path('groupmgmt/<int:pk>/delete/', group_delete, name='group_mgmt_delete'),
    path('groupmgmt/<int:pk>/', group_detail, name='group_mgmt_detail'),
    path('ops_group_mgmt', ops_group_mgmt, name='ops_group_mgmt'),
    path('group_mgmt/restore_deleted_groups/', restore_deleted_groups, name='restore_deleted_groups'),
    path('bulk_ops_group_mgmt', bulk_ops_group_mgmt, name='bulk_ops_group_mgmt'),
    path('groupmgmt/<int:pk>/list_users/', group_mgmt_list_users, name='group_mgmt_list_users'),
    
]