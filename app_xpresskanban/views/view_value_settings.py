# Create your views here.
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mptt.exceptions import InvalidMove
from copy import copy
from copy import deepcopy
from mptt.exceptions import InvalidMove
from mptt.utils import tree_item_iterator
from mptt.templatetags.mptt_tags import cache_tree_children
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User, Group
import ast
import csv
from django.db.models import Q
from ..forms import *
import datetime
from ..decorators import *
# declare the different types of dynamic CRUD
def get_model_class(value_type):
    model_classes = {
        'Project': Project,
        'Product': Product,
        'Service': Service,
        'Solution': Solution,
        'ValueStream': ValueStream,
        'Organization': Organization,
        'Team': Team,
        # Add more mappings if needed
    }
    return model_classes.get(value_type)

################################################################################
#
# Settings for the Project/Product/Service/Solution/ValueStream/Team/Organization
#
################################################################################
@login_required(login_url='login')
@check_value_permissions_type('edit')
def value_settings_main(request, value_type, pk):
    model_name = value_type
    model_class = None
    item_count = 0
    model_class = get_model_class(model_name)
    obj = get_object_or_404(model_class, pk=pk)

    entered_user = None
    entered_user_groups = None

    users_in_view_group = None
    users_in_edit_group = None
    users_in_admin_group = None

    view_group = f"{value_type}_{pk}_view"
    edit_group = f"{value_type}_{pk}_edit"
    admin_group = f"{value_type}_{pk}_admin"
    # Get or create the groups if they don't exist
    view_group1, created = CustomGroup.objects.get_or_create(name=view_group)
    edit_group1, created = CustomGroup.objects.get_or_create(name=edit_group)
    admin_group1, created = CustomGroup.objects.get_or_create(name=admin_group)
    print(">>> === VIEW GROUP {view_group1} {created}, {edit_group1}, {admin_group1} === <<<")
    # send the users list for each view, edit, admin group to template
    users_in_view_group = User.objects.filter(groups=view_group1)
    users_in_edit_group = User.objects.filter(groups=edit_group1)
    users_in_admin_group = User.objects.filter(groups=admin_group1)
    ################################################################################
    if request.method == 'POST':
        view_membership = request.POST.get('view_membership')
        edit_membership = request.POST.get('edit_membership')
        admin_membership = request.POST.get('admin_membership')
        viewers = [euser.strip() for euser in view_membership.split(',')]
        editors = [euser.strip() for euser in edit_membership.split(',')]
        admins = [euser.strip() for euser in admin_membership.split(',')]

        for viewer in viewers:
            entered_user = User.objects.filter(username=viewer).first()
            if entered_user != None:
                entered_user.groups.add(view_group1)
        for editor in editors:
            entered_user = User.objects.filter(username=editor).first()
            if entered_user != None:
                #entered_user.groups.add(view_group1)
                entered_user.groups.add(edit_group1)
        for admin in admins:
            entered_user = User.objects.filter(username=admin).first()
            if entered_user != None:
                #entered_user.groups.add(view_group1)
                #entered_user.groups.add(edit_group1)
                entered_user.groups.add(admin_group1)
        
        # send the users list for each view, edit, admin group to template
        users_in_view_group = User.objects.filter(groups=view_group1)
        users_in_edit_group = User.objects.filter(groups=edit_group1)
        users_in_admin_group = User.objects.filter(groups=admin_group1)

        print(f">>> === CHECKING {users_in_view_group} === <<<")
    ################################################################################
    context = {'value_type': value_type, 'pk': pk, 'object': obj, 
               'entered_user': entered_user,'entered_user_groups': entered_user_groups,
               'users_in_view_group':users_in_view_group,'users_in_edit_group':users_in_edit_group,
               'users_in_admin_group':users_in_admin_group,
               'page': 'Value Settings', 'active_tab': 'members'}
    return render(request, 'app_xpresskanban/value_crud/value_settings.html', context)


################################################################################
#
# Settings for the Board
#
################################################################################
@login_required(login_url='login')
@check_board_permissions_type('edit')
def board_settings_main(request, value_type, pk, board_id):
    model_name = value_type
    model_class = None
    item_count = 0
    model_class = get_model_class(model_name)
    item_class = Board
    obj = get_object_or_404(model_class, pk=pk)
    item = get_object_or_404(item_class, id=board_id)

    entered_user = None
    entered_user_groups = None

    users_in_view_group = None
    users_in_edit_group = None
    users_in_admin_group = None

    view_group = f"Board_{board_id}_{value_type}_{pk}_view"
    edit_group = f"Board_{board_id}_{value_type}_{pk}_edit"
    admin_group = f"Board_{board_id}_{value_type}_{pk}_admin"
    # Get or create the groups if they don't exist
    view_group1, created = CustomGroup.objects.get_or_create(name=view_group)
    edit_group1, created = CustomGroup.objects.get_or_create(name=edit_group)
    admin_group1, created = CustomGroup.objects.get_or_create(name=admin_group)
    print(">>> === VIEW GROUP {view_group1} {created}, {edit_group1}, {admin_group1} === <<<")
    # send the users list for each view, edit, admin group to template
    users_in_view_group = User.objects.filter(groups=view_group1)
    users_in_edit_group = User.objects.filter(groups=edit_group1)
    users_in_admin_group = User.objects.filter(groups=admin_group1)
    ################################################################################
    if request.method == 'POST':
        view_membership = request.POST.get('view_membership')
        edit_membership = request.POST.get('edit_membership')
        admin_membership = request.POST.get('admin_membership')
        viewers = [euser.strip() for euser in view_membership.split(',')]
        editors = [euser.strip() for euser in edit_membership.split(',')]
        admins = [euser.strip() for euser in admin_membership.split(',')]

        for viewer in viewers:
            entered_user = User.objects.filter(username=viewer).first()
            if entered_user != None:
                entered_user.groups.add(view_group1)
        for editor in editors:
            entered_user = User.objects.filter(username=editor).first()
            if entered_user != None:
                #entered_user.groups.add(view_group1)
                entered_user.groups.add(edit_group1)
        for admin in admins:
            entered_user = User.objects.filter(username=admin).first()
            if entered_user != None:
                #entered_user.groups.add(view_group1)
                #entered_user.groups.add(edit_group1)
                entered_user.groups.add(admin_group1)
        
        # send the users list for each view, edit, admin group to template
        users_in_view_group = User.objects.filter(groups=view_group1)
        users_in_edit_group = User.objects.filter(groups=edit_group1)
        users_in_admin_group = User.objects.filter(groups=admin_group1)

        print(f">>> === CHECKING {users_in_view_group} === <<<")
    ################################################################################
    context = {'value_type': value_type, 'pk': pk, 'object': obj, 'item':item,
               'entered_user': entered_user,'entered_user_groups': entered_user_groups,
               'users_in_view_group':users_in_view_group,'users_in_edit_group':users_in_edit_group,
               'users_in_admin_group':users_in_admin_group,
               'page': 'Value Settings', 'active_tab': 'members'}
    return render(request, 'app_xpresskanban/board_settings/board_settings.html', context)


################################################################################
#
# Remove User from the Group
#
################################################################################
@login_required(login_url='login')
@user_in_group(['View_Value_Group'])
def remove_user_from_group(request, value_type, pk, board_id):
    model_name = value_type
    model_class = None
    item_count = 0
    model_class = get_model_class(model_name)
    item_class = Board
    obj = get_object_or_404(model_class, pk=pk)
    item = get_object_or_404(item_class, id=board_id)

    users_in_view_group = None
    users_in_edit_group = None
    users_in_admin_group = None

    view_group = f"Board_{board_id}_{value_type}_{pk}_view"
    edit_group = f"Board_{board_id}_{value_type}_{pk}_edit"
    admin_group = f"Board_{board_id}_{value_type}_{pk}_admin"
    # Get or create the groups if they don't exist
    view_group1, created = CustomGroup.objects.get_or_create(name=view_group)
    edit_group1, created = CustomGroup.objects.get_or_create(name=edit_group)
    admin_group1, created = CustomGroup.objects.get_or_create(name=admin_group)
    # send the users list for each view, edit, admin group to template
    users_in_view_group = User.objects.filter(groups=view_group1)
    users_in_edit_group = User.objects.filter(groups=edit_group1)
    users_in_admin_group = User.objects.filter(groups=admin_group1)

    url_ref = reverse('board_settings', args=[model_name, pk, board_id])
    if request.method == 'POST':
        remove_user_id= request.POST.get('remove_user_id')
        from_group_name = request.POST.get('from_user_group')
        if remove_user_id != None and from_group_name != None:
            print(f">>> === FROM GROUP NAME: {from_group_name} === <<<")
            # Get the group object
            print(f">>> === REMOVE USER {remove_user_id} FROM GROUP {from_group_name} === <<<")
            group = CustomGroup.objects.get(name=from_group_name)    
            # Remove the user from the group
            remove_user_obj = User.objects.get(id=remove_user_id)
            remove_user_obj.groups.remove(group)
            return redirect(url_ref)
      
    print(f">>> === CHECKING {users_in_view_group} === <<<")
    ################################################################################
    context = {'value_type': value_type, 'pk': pk, 'object': obj, 'item':item,              
               'users_in_view_group':users_in_view_group,'users_in_edit_group':users_in_edit_group,
               'users_in_admin_group':users_in_admin_group,
               'page': 'Value Settings', 'active_tab': 'members'}
    return render(request, 'app_xpresskanban/board_settings/board_settings.html', context)

################################################################################
#
# Remove Value Type - User from the Group
#
################################################################################
@login_required(login_url='login')
@user_in_group(['View_Value_Group'])
def val_remove_user_from_group(request, value_type, pk):
    model_name = value_type
    model_class = None
    item_count = 0
    model_class = get_model_class(model_name)
    obj = get_object_or_404(model_class, pk=pk)

    users_in_view_group = None
    users_in_edit_group = None
    users_in_admin_group = None

    view_group = f"{value_type}_{pk}_view"
    edit_group = f"{value_type}_{pk}_edit"
    admin_group = f"{value_type}_{pk}_admin"
    # Get or create the groups if they don't exist
    view_group1, created = CustomGroup.objects.get_or_create(name=view_group)
    edit_group1, created = CustomGroup.objects.get_or_create(name=edit_group)
    admin_group1, created = CustomGroup.objects.get_or_create(name=admin_group)
    # send the users list for each view, edit, admin group to template
    users_in_view_group = User.objects.filter(groups=view_group1)
    users_in_edit_group = User.objects.filter(groups=edit_group1)
    users_in_admin_group = User.objects.filter(groups=admin_group1)

    url_ref = reverse('value_settings', args=[model_name, pk])
    if request.method == 'POST':
        remove_user_id= request.POST.get('remove_user_id')
        from_group_name = request.POST.get('from_user_group')
        if remove_user_id != None and from_group_name != None:
            print(f">>> === FROM GROUP NAME: {from_group_name} === <<<")
            # Get the group object
            print(f">>> === REMOVE USER {remove_user_id} FROM GROUP {from_group_name} === <<<")
            group = CustomGroup.objects.get(name=from_group_name)    
            # Remove the user from the group
            remove_user_obj = User.objects.get(id=remove_user_id)
            remove_user_obj.groups.remove(group)
            return redirect(url_ref)
      
    print(f">>> === CHECKING {users_in_view_group} === <<<")
    ################################################################################
    context = {'value_type': value_type, 'pk': pk, 'object': obj,              
               'users_in_view_group':users_in_view_group,'users_in_edit_group':users_in_edit_group,
               'users_in_admin_group':users_in_admin_group,
               'page': 'Value Settings', 'active_tab': 'members'}
    return render(request, 'app_xpresskanban/value_crud/value_settings.html', context)