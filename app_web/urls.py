from django.urls import path

from . import views
from .views_ext import canvas_views

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
    path('cafe_wbs/', views.cafe_wbs, name="cafe_wbs"),
    
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
    path('dev_trx_view_agree_on_canvas/<int:canvas_id>/', canvas_views.dev_trx_view_agree_on_canvas, name='dev_trx_view_agree_on_canvas'),
    path('dev_trx_edit_canvas/<int:canvas_id>/', canvas_views.dev_trx_edit_canvas, name='dev_trx_edit_canvas'),
    path('dev_trx_delete_canvas/<int:canvas_id>/', canvas_views.dev_trx_delete_canvas, name='dev_trx_delete_canvas'),
]

