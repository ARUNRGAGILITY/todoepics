from django.urls import path

from . import views
from .views_ext import canvas_views
from app_baseline.urls.base import urls_base
urlpatterns = [
    # all users will come to this visitor page
    path('', views.welcome, name="welcome"),
    # if login needed login page displayed
    path('login/', views.login_page, name="login"),
    # if registeration needed registration page displayed
    path('register/', views.register, name="register"),
    # user has logged in
    path('user-page/', views.user_page, name="user_page"),
    # logout page
    path('logout_page/', views.logout_page, name="logout_page"),
    # profile page
    path('profile_page/', views.profile_page, name="profile_page"),
    # edit profile page
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    # admin page
    path('admin_page/', views.admin_page, name="admin_page"),
    
    ###########################################################
    # roles page
    path('roles_mgmt/', views.roles_mgmt, name="roles_mgmt"),
    ###########################################################
    # value stream page: ops and dev
    path('ops_valuestream_mgmt/', views.ops_valuestream_mgmt, name="ops_valuestream_mgmt"),
    path('dev_valuestream_mgmt/<int:id>/', views.dev_valuestream_mgmt, name="dev_valuestream_mgmt"),
    path('valuestream_steps/<str:vs>/<int:id>/', views.valuestream_steps, name="valuestream_steps"),
    path('edit_dev_valuestream/<int:id>/', views.edit_dev_valuestream, name="edit_dev_valuestream"),
    path('edit_ops_valuestream/<int:id>/', views.edit_ops_valuestream, name="edit_ops_valuestream"),
    path('valuestream_mgmt/', views.valuestream_mgmt, name="valuestream_mgmt"),
    path('view_ops_valuestream/<int:id>/', views.view_ops_valuestream, name="view_ops_valuestream"),
    path('view_step/<str:vs>/<int:ref_id>/<int:id>/', views.view_step, name="view_step"),
    path('summary_ops_valuestream/<int:id>/', views.summary_ops_valuestream, name="summary_ops_valuestream"),
    path('view_dev_valuestream/<int:id>/', views.view_dev_valuestream, name="view_dev_valuestream"),
    path('summary_dev_valuestream/<int:id>/', views.summary_dev_valuestream, name="summary_dev_valuestream"),
    path('edit_step/<str:vs>/<int:ref_id>/<int:id>/', views.edit_step, name="edit_step"),
    path('delete_ovs/<int:id>/', views.delete_ovs, name="delete_ovs"),
    path('add_ovs/', views.add_ovs, name="add_ovs"),
    path('add_dvs/<int:id>/', views.add_dvs, name="add_dvs"),
    path('sorted_vsm_steps/', views.sorted_vsm_steps, name="sorted_vsm_steps"),
    path('ajaxupdate_valuestream_steps/', views.ajaxupdate_valuestream_steps, name="ajaxupdate_valuestream_steps"),
    path('add_vsm_steps/<str:vs>/<int:id>/', views.add_vsm_steps, name="add_vsm_steps"),
    path('delete_step/<str:vs>/<int:ref_id>/<int:id>/', views.delete_step, name="delete_step"),
    path('show_ovs_step_details/<int:id>/', views.show_ovs_step_details, name="show_ovs_step_details"),
    path('show_dvs_step_details/<int:ref_id>/<int:id>/', views.show_dvs_step_details, name="show_dvs_step_details"),
    #############################################################
    # cafe
    path('cafe_start/', views.cafe_start, name="cafe_start"),
    path('index_st/', views.index_st, name="index_st"),
    path('st_detail/<int:theme_id>/', views.st_detail, name='st_detail'),
    path('cafe_wbs/<int:id>/', views.cafe_wbs, name="cafe_wbs"),
    
    # Value stream canvas
    path('home_valuestream/', views.home_valuestream, name="home_valuestream"),
    
    # Value stream canvas
    path('home_devvaluestream_canvas/', views.home_devvaluestream_canvas, name="home_devvaluestream_canvas"),
    path('list_devvaluestream_canvas/', views.list_devvaluestream_canvas, name="list_devvaluestream_canvas"),
    # portfolio 
    path('home_portfolio_canvas/', views.home_portfolio_canvas, name="home_portfolio_canvas"),
    path('list_portfolio_canvas/', views.list_portfolio_canvas, name="list_portfolio_canvas"),
    path('show_portfolio_canvas/<int:id>/', views.show_portfolio_canvas, name="show_portfolio_canvas"),
    
    
    ## main page
    ## website/like/agiletia.com
    
    path('vsm/', views.vsm, name="vsm"),
    path('cafe/', views.cafe, name="cafe"),
    path('help/', views.help, name="help"),
    path('beaiagile/', views.beaiagile, name="beaiagile"),
    path('about/', views.about, name="about"),
    path('organization_transformation/', views.organization_transformation, name="organization_transformation"),
    path('transformation_leadership/', views.transformation_leadership, name="transformation_leadership"),
    path('transformation_sw_training_services/', views.transformation_sw_training_services, name="transformation_sw_training_services"),
    
    # transformation canvas for ops and dev
    path('ops_trx_add_canvas/<int:id>/', canvas_views.ops_trx_add_canvas, name='ops_trx_add_canvas'),
    path('ops_trx_list_canvas/<int:id>/', canvas_views.ops_trx_list_canvas, name='ops_trx_list_canvas'),
    path('ops_trx_view_canvas/<int:canvas_id>/', canvas_views.ops_trx_view_canvas, name='ops_trx_view_canvas'),
    path('ops_trx_edit_canvas/<int:canvas_id>/', canvas_views.ops_trx_edit_canvas, name='ops_trx_edit_canvas'),
    path('ops_trx_delete_canvas/<int:canvas_id>/', canvas_views.ops_trx_delete_canvas, name='ops_trx_delete_canvas'),
    
    path('ajax_update_dtc_field/', canvas_views.ajax_update_dtc_field, name='ajax_update_dtc_field'),
    path('dev_trx_add_canvas/<int:id>/', canvas_views.dev_trx_add_canvas, name='dev_trx_add_canvas'),
    path('dev_trx_list_canvas/<int:id>/', canvas_views.dev_trx_list_canvas, name='dev_trx_list_canvas'),
    path('dev_trx_view_canvas/<int:canvas_id>/', canvas_views.dev_trx_view_canvas, name='dev_trx_view_canvas'),
    path('dev_trx_view_canvas_we/<int:canvas_id>/', canvas_views.dev_trx_view_canvas_we, name='dev_trx_view_canvas_we'),
    path('dev_trx_view_canvas_pdf/<int:canvas_id>/', canvas_views.dev_trx_view_canvas_pdf, name='dev_trx_view_canvas_pdf'),
    path('dev_trx_view_agree_on_canvas/<int:canvas_id>/', canvas_views.dev_trx_view_agree_on_canvas, name='dev_trx_view_agree_on_canvas'),
    path('dev_trx_edit_canvas/<int:canvas_id>/', canvas_views.dev_trx_edit_canvas, name='dev_trx_edit_canvas'),
    path('dev_trx_delete_canvas/<int:canvas_id>/', canvas_views.dev_trx_delete_canvas, name='dev_trx_delete_canvas'),
    
    
    # setting up general ui/ux and access links for the users
    # profile
    path('my_profile_page/', views.my_profile_page, name="my_profile_page"),
    path('my_settings_page/', views.my_settings_page, name="my_settings_page"),
    path('my_workspace_page/', views.my_workspace_page, name="my_workspace_page"),
    
    path('my_kanban/', views.my_kanban, name="my_kanban"),
    path('my_todolist/', views.my_todolist, name="my_todolist"),
    path('my_checklist/', views.my_checklist, name="my_checklist"),
    path('my_projects/', views.my_projects, name="my_projects"),
    
    path('my_roles_page/', views.my_roles_page, name="my_roles_page"),
    path('my_admin_roles/', views.my_admin_roles, name="my_admin_roles"),
    path('my_project_roles/', views.my_project_roles, name="my_project_roles"),
    
    path('my_organizations_page/', views.my_organizations_page, name="my_organizations_page"),
    path('my_authorized_organizations/', views.my_authorized_organizations, name="my_authorized_organizations"),
    path('my_viewable_organizations/', views.my_viewable_organizations, name="my_viewable_organizations"),
    
    # ADMIN ROLES
    path('site_admin_home/', views.site_admin_home, name="site_admin_home"),
    path('ajax-user-suggestions/', views.ajax_user_suggestions, name='ajax-user-suggestions'),
    path('ajax_add_org_admin/', views.ajax_add_org_admin, name="ajax_add_org_admin"),
    path('ajax_delete_org_admin/', views.ajax_delete_org_admin, name="ajax_delete_org_admin"),
    path('add_organization/', views.add_organization, name="add_organization"),
    path('delete_organization/<int:id>', views.delete_organization, name="delete_organization"),
    path('edit_organization/<int:id>', views.edit_organization, name="edit_organization"),
    path('view_organization/<int:id>', views.view_organization, name="view_organization"),
    
    path('org_admin_home/', views.org_admin_home, name="org_admin_home"),
    path('ajax_add_project_admin/', views.ajax_add_project_admin, name="ajax_add_project_admin"),
    path('ajax_delete_project_admin/', views.ajax_delete_project_admin, name="ajax_delete_project_admin"),
    
    # ORGANIZATION VIEWING
    path('organization_page/<int:id>/', views.organization_page, name="organization_page"),
    path('organization_admin_page/<int:id>/', views.organization_admin_page, name="organization_admin_page"),
    path('organization_wbs_page/<int:id>/', views.organization_wbs_page, name="organization_wbs_page"),
    path('organization_big_picture/<int:id>/', views.organization_big_picture, name="organization_big_picture"),
    path('organization_ref_arch/<int:id>/', views.organization_ref_arch, name="organization_ref_arch"),
]

urlpatterns += urls_base.urlpatterns_base