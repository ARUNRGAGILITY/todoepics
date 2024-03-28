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
# Create your views here.
# ops of the planner
@login_required(login_url='login')
def kanban_home(request):
    context = {'page': 'Kanban', 'active_tab': 'kanban'}
    return render(request, 'app_xpresskanban/kanban_home.html', context)
@login_required(login_url='login')
def create_value(request, value_type):
    context = {'page': 'Create Value', 'active_tab': 'create_value',
               'value_type': value_type}
    return render(request, 'app_xpresskanban/create_value.html', context)


## GOALS ##

from django.shortcuts import render

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

from app_xpresskanban.decorators import *
from app_baseline.models.user.model_user import *
# Assuming you have your models (Project, Product, Service, Solution) defined as before
# ... Other view functions ...
######################################## Begin User Mgmt CRUD ############################
@login_required(login_url='login')
def main_home(request):
    context = { 'page': 'Main MVP', 'active_tab': 'MainMVP'}
    return render(request, 'main_mvp/home.html', context)

@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def user_list(request):
    query = ''
    users = User.objects.filter(is_active=True)
    
     # pagination
    pagination_on = False
    selected_pagination = request.GET.get('pagination', 'all')
    #selected_pagination = 'all'
    if selected_pagination == 'all':
        paginated_items = users
        pagination_on = False
    else:
        pagination_on = True
        items_per_page = int(selected_pagination) 
        paginator = Paginator(users, items_per_page)        

        page_number = request.GET.get('page')
        try:
            paginated_items = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_items = paginator.page(1)
        except EmptyPage:
            paginated_items = paginator.page(paginator.num_pages)
    
    context = {'page': 'User List', 'active_tab': 'user_mgmt_list', 
                   'users': users, 'query': query,
                   'pagination':selected_pagination, 
                   'paginated_items': paginated_items, 'pagination_on': pagination_on}

    if request.method == 'POST':
        query = request.POST.get('q')
        if query:
            #users = User.objects.filter(username__icontains=query)
            users = User.objects.filter(
                    Q(username__icontains=query) |
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(email__icontains=query))
        else:
            users = User.objects.filter(is_active=True)
        if query is None:
            query = ''
        # pagination
        pagination_on = False
        selected_pagination = request.GET.get('pagination', 'all')
        #selected_pagination = 'all'
        if selected_pagination == 'all':
            paginated_items = users
            pagination_on = False
        else:
            pagination_on = True
            items_per_page = int(selected_pagination) 
            paginator = Paginator(users, items_per_page)        

            page_number = request.GET.get('page')
            try:
                paginated_items = paginator.page(page_number)
            except PageNotAnInteger:
                paginated_items = paginator.page(1)
            except EmptyPage:
                paginated_items = paginator.page(paginator.num_pages)
        
        context = {'page': 'User List', 'active_tab': 'user_mgmt_list', 
                    'users': users, 'query': query,
                    'pagination':selected_pagination, 
                    'paginated_items': paginated_items, 'pagination_on': pagination_on}
       
        return render(request, 'role_based_templates/user_mgmt/user_mgmt_list.html', context)
    else:
        return render(request, 'role_based_templates/user_mgmt/user_mgmt_list.html', context)

@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def restore_user_list(request):
    query = ''
    users = User.objects.filter(is_active=False)
    
     # pagination
    pagination_on = False
    selected_pagination = request.GET.get('pagination', 'all')
    #selected_pagination = 'all'
    if selected_pagination == 'all':
        paginated_items = users
        pagination_on = False
    else:
        pagination_on = True
        items_per_page = int(selected_pagination) 
        paginator = Paginator(users, items_per_page)        

        page_number = request.GET.get('page')
        try:
            paginated_items = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_items = paginator.page(1)
        except EmptyPage:
            paginated_items = paginator.page(paginator.num_pages)
    
    context = {'page': 'User List', 'active_tab': 'user_mgmt_list', 
                   'users': users, 'query': query,
                   'pagination':selected_pagination, 
                   'paginated_items': paginated_items, 'pagination_on': pagination_on}

    if request.method == 'POST':
        query = request.POST.get('q')
        if query:
            #users = User.objects.filter(username__icontains=query)
            users = User.objects.filter(
                    Q(username__icontains=query) |
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(email__icontains=query))
        else:
            users = User.objects.filter(is_active=False)
        if query is None:
            query = ''
        # pagination
        pagination_on = False
        selected_pagination = request.GET.get('pagination', 'all')
        #selected_pagination = 'all'
        if selected_pagination == 'all':
            paginated_items = users
            pagination_on = False
        else:
            pagination_on = True
            items_per_page = int(selected_pagination) 
            paginator = Paginator(users, items_per_page)        

            page_number = request.GET.get('page')
            try:
                paginated_items = paginator.page(page_number)
            except PageNotAnInteger:
                paginated_items = paginator.page(1)
            except EmptyPage:
                paginated_items = paginator.page(paginator.num_pages)
        
        context = {'page': 'User List', 'active_tab': 'user_mgmt_list', 
                    'users': users, 'query': query,
                    'pagination':selected_pagination, 
                    'paginated_items': paginated_items, 'pagination_on': pagination_on}
       
        return render(request, 'role_based_templates/user_mgmt/user_mgmt_restore.html', context)
    else:
        return render(request, 'role_based_templates/user_mgmt/user_mgmt_restore.html', context)


@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def restore_deleted_groups(request):
    query = ''
    group_object = CustomGroup
    users = User.objects.filter(is_active=False)
    groups = group_object.objects.filter(active=False)
     # pagination
    pagination_on = False
    selected_pagination = request.GET.get('pagination', 'all')
    #selected_pagination = 'all'
    if selected_pagination == 'all':
        paginated_items = groups
        pagination_on = False
    else:
        pagination_on = True
        items_per_page = int(selected_pagination) 
        paginator = Paginator(groups, items_per_page)        

        page_number = request.GET.get('page')
        try:
            paginated_items = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_items = paginator.page(1)
        except EmptyPage:
            paginated_items = paginator.page(paginator.num_pages)
    
    context = {'page': 'Group List', 'active_tab': 'restore_deleted_groups', 
                   'users': users, 'query': query,
                   'groups': groups,
                   'pagination':selected_pagination, 
                   'paginated_items': paginated_items, 'pagination_on': pagination_on}

    if request.method == 'POST':
        query = request.POST.get('q')
        if query:
            groups = group_object.objects.filter(
                    Q(name__icontains=query) )              
        else:
            groups = group_object.objects.filter(active=False)
        if query is None:
            query = ''
        # pagination
        pagination_on = False
        selected_pagination = request.GET.get('pagination', 'all')
        #selected_pagination = 'all'
        if selected_pagination == 'all':
            paginated_items = groups
            pagination_on = False
        else:
            pagination_on = True
            items_per_page = int(selected_pagination) 
            paginator = Paginator(groups, items_per_page)        

            page_number = request.GET.get('page')
            try:
                paginated_items = paginator.page(page_number)
            except PageNotAnInteger:
                paginated_items = paginator.page(1)
            except EmptyPage:
                paginated_items = paginator.page(paginator.num_pages)
        
        context = {'page': 'User List', 'active_tab': 'user_mgmt_list', 
                    'users': users, 'query': query,
                    'pagination':selected_pagination, 
                    'paginated_items': paginated_items, 'pagination_on': pagination_on}
       
        return render(request, 'role_based_templates/group_mgmt/group_mgmt_restore.html', context)
    else:
        return render(request, 'role_based_templates/group_mgmt/group_mgmt_restore.html', context)


@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def user_detail(request,pk):
    context = {'page': 'User Details'}
    user = get_object_or_404(User, pk=pk)
    context = {'user':user, 'active_tab':'user_details'}
    return render(request, 'role_based_templates/user_mgmt/user_mgmt_details.html', context)

@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def user_home(request):
    context = {'page': 'User Home'}
    return render(request, 'role_based_templates/user_mgmt/user_mgmt_home.html', context)

@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def user_delete(request, pk):
    context = {'page': 'User Home'}
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = DeleteUserConfirmationForm(request.POST)
        if form.is_valid():
            user.is_active = False
            user.save()
            return redirect('user_mgmt_list') 
    else:
        form = DeleteUserConfirmationForm()
    context = {
        'active_tab': 'delete_user',
        'delete_user': user,
    }
    return render(request, 'role_based_templates/user_mgmt/user_mgmt_confirm_delete.html', context)

@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def user_update(request, pk):
    context = {'page': 'User Home'}
    form = UserUpdateForm()
    list = get_object_or_404(User, id=pk)
    print(f">>> === USER UPDATE INFO & GROUP CHECK {list} === <<<")
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=list)
        if form.is_valid():
            user = form.save()
            # Update user's groups
            updated_groups = form.cleaned_data['groups']
            user.groups.set(updated_groups)
            print(f">>> === USER UPDATE INFO & GROUP CHECK {user.groups} === <<<")
            return redirect('user_mgmt_list') 
    else:
        form = UserUpdateForm(instance=list)
    context = {
        'active_tab': 'update_user',
        'form': form,
    }
    return render(request, 'role_based_templates/user_mgmt/user_mgmt_update.html', context)

@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def user_create(request):
    context = {'page': 'User Home', 'active_tab': "add_user"}
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.instance.first_name = form.cleaned_data['first_name']
            form.instance.last_name = form.cleaned_data['last_name']
            user = form.save()
            selected_groups = request.POST.getlist('groups')  
            got_selected_groups = get_selected_group_details(selected_groups)
            for group_name in got_selected_groups:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)       
            print(f">>>>>> SELECTED GROUPS {selected_groups} ==> details {got_selected_groups}")
            return redirect('user_mgmt_list') 
    else:
        form = UserRegisterForm()
    context = {
        'active_tab': 'add_user',
        'form': form,
    }
    return render(request, 'role_based_templates/user_mgmt/user_mgmt_add.html', context)
@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def user_create_multiple(request):
    context = {'page': 'User Home', 'active_tab': "add_multiple_users"}
    add_multiple_users_csv = None
    if request.method == 'POST':
        add_multiple_users_csv = request.POST['add_multiple_users_csv']
        arr_musers = add_multiple_users_csv.split('\n')
        for euser in arr_musers:
            print(f"====> {euser}")
            csv_data = csv.reader([euser])
            arr_user = next(csv_data)
            user_firstname, user_lastname, user_username, user_email, user_password, user_groups_text = arr_user
            print(f">>>>> groups_text {user_groups_text}")
            user_groups = ast.literal_eval(user_groups_text)
            user = User.objects.create_user(
                first_name = user_firstname,
                last_name = user_lastname,
                username=user_username,
                email=user_email,
                password=user_password
            )     
            for group_name in user_groups:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)       
            return redirect('user_mgmt_list') 
    context = {
        'active_tab': 'add_multiple_users',
        'add_multiple_users_csv': add_multiple_users_csv,
    }
    return render(request, 'role_based_templates/user_mgmt/user_mgmt_add_multiple.html', context)

# ops of the planner
@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def bulk_ops_user_mgmt(request):
    group_object = CustomGroup
    groups = group_object.objects.all()
    if request.method == 'POST':
        groups = group_object.objects.all()
        selected_group = None
        form_data = request.POST
        selected_object_ids = request.POST.getlist('obj_box')   
        selected_objects = get_selected_users_details(selected_object_ids)
        print(f">>>>> BULK {selected_object_ids} for the bulk user_mgmt ops")     
        bulk_obj_ops = form_data.get('bulk_obj_ops')
       
        print(f">>> which group {selected_group}")
        if bulk_obj_ops == "bulk_move":
            for id in selected_object_ids:
                selected_group_name = form_data.get('selected_group')
                selected_group = group_object.objects.get(name=selected_group_name)
                selected_group_id = selected_group.id
                print(f">>>>>>>>>>> CHECK {id} ==> {selected_object_ids}")
                user = User.objects.get(id=id)
                user.groups.add(selected_group_id)
                user_groups = user.groups.all()
                print(f">>>>> USER GROUPS: {user_groups}")
        if bulk_obj_ops == "bulk_remove":
            for id in selected_object_ids:
                selected_group_name = form_data.get('selected_group')
                selected_group = group_object.objects.get(name=selected_group_name)
                selected_group_id = selected_group.id
                print(f">>>>>>>>>>> CHECK {id} ==> {selected_object_ids}")
                user = User.objects.get(id=id)
                user.groups.remove(selected_group_id)
                user_groups = user.groups.all()
                print(f">>>>> USER GROUPS: {user_groups}")
        elif bulk_obj_ops == "bulk_delete":
            print(f">>>>> INSDIE THE SOFT DELETE  {bulk_obj_ops}")
            for id in selected_object_ids:
                user = User.objects.get(id=id)
                user.is_active=False
                user.save()
                print(f">>>>> INSDIE THE SOFT DELETE  /{user} /{id} /{user.is_active}")
        elif bulk_obj_ops == "bulk_restore":
            print(f">>>>> INSDIE THE RESTORE {bulk_obj_ops}")
            for id in selected_object_ids:
                user = User.objects.get(id=id)
                user.is_active=True
                user.save()
                print(f">>>>> INSDIE THE SOFT DELETE  /{user} /{id} /{user.is_active}")
        elif bulk_obj_ops == "bulk_delete_permanently":
            print(f">>>>> INSDIE THE RESTORE {bulk_obj_ops}")
            for id in selected_object_ids:
                user = User.objects.get(id=id)
                user.delete()

        context = {'bulk_obj_ops': bulk_obj_ops, 
                   'selected_objects': selected_objects,
                   'selected_object_ids':selected_object_ids,
                   'groups':groups}
    return redirect("user_mgmt_list")


# ops of the planner
@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def bulk_ops_group_mgmt(request):
    group_object = CustomGroup
    groups = group_object.objects.all()
    if request.method == 'POST':
        groups = group_object.objects.all()
        selected_group = None
        form_data = request.POST
        selected_object_ids = request.POST.getlist('obj_box')   
        selected_objects = get_selected_group_details(selected_object_ids)
        print(f">>>>> BULK {selected_object_ids} for the bulk group_mgmt ops")     
        bulk_obj_ops = form_data.get('bulk_obj_ops')
       
        print(f">>> which group {selected_group}")       
        if bulk_obj_ops == "bulk_restore":
            print(f">>>>> INSDIE THE RESTORE GROUP {bulk_obj_ops}")
            for id in selected_object_ids:
                group = group_object.objects.get(id=id)
                group.active=True
                group.save()
                print(f">>>>> INSDIE THE SOFT DELETE  /{group} /{id} /{group.active}")
        elif bulk_obj_ops == "bulk_delete_permanently":
            print(f">>>>> INSDIE THE RESTORE {bulk_obj_ops}")
            for id in selected_object_ids:
                group = group_object.objects.get(id=id)
                group.deleted = True

        context = {'bulk_obj_ops': bulk_obj_ops, 
                   'selected_objects': selected_objects,
                   'selected_object_ids':selected_object_ids,
                   'groups':groups}
    return redirect("group_mgmt_list")



# ops of the planner
@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def ops_user_mgmt(request):
    group_object=CustomGroup
    groups = group_object.objects.all()
    if request.method == 'POST':
        groups = group_object.objects.all()
        form_data = request.POST
        selected_object_ids = request.POST.getlist('obj_box')   
        selected_objects = get_selected_users_details(selected_object_ids)
        print(f">>>>> {selected_object_ids} for the bulk user_mgmt ops")     
        bulk_obj_ops = form_data.get('bulk_obj_ops')
        if bulk_obj_ops == "bulk_move":
            for id in selected_object_ids:
                User.objects.filter(id=id)
        if bulk_obj_ops == "bulk_remove":
            for id in selected_object_ids:
                User.objects.filter(id=id)
        elif bulk_obj_ops == "delete":
            for id in selected_object_ids:
                User.objects.filter(id=id).update(active=False, deleted=False,  )
       
        context = {'bulk_obj_ops': bulk_obj_ops, 
                   'selected_objects': selected_objects,
                   'selected_object_ids':selected_object_ids,
                   'groups':groups}
    return render(request, 'role_based_templates/user_mgmt/ops_user_mgmt.html', context)

# ops of the planner
@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def ops_group_mgmt(request):
    group_object=CustomGroup
    groups = group_object.objects.filter(active=True)
    if request.method == 'POST':
        groups = group_object.objects.filter(active=True)
        form_data = request.POST
        selected_object_ids = request.POST.getlist('obj_box')   
        selected_objects = get_selected_group_details(selected_object_ids)
        print(f">>>>> {selected_object_ids} for the bulk group_mgmt ops")     
        bulk_obj_ops = form_data.get('bulk_obj_ops')       
        if bulk_obj_ops == "bulk_delete":
            for id in selected_object_ids:
                group_object.objects.filter(id=id).update(active=False, deleted=False,  )
                print(f">>> === {id} delete group === <<<")
        context = {'bulk_obj_ops': bulk_obj_ops, 
                   'selected_objects': selected_objects,
                   'selected_object_ids':selected_object_ids,
                   'groups':groups}
    #return render(request, 'role_based_templates/group_mgmt/ops_group_mgmt.html', context)
    return redirect('group_mgmt_list')

def get_selected_group_details(selected_groups):
    group_object=CustomGroup
    all_groups = group_object.objects.all()
    return_selected_groups = []
    for group_id in selected_groups:
        group = get_object_or_404(all_groups, pk=group_id)
        return_selected_groups.append(group)
    return return_selected_groups

def get_selected_users_details(selected_ids):
    # Retrieve all users
    all_users = User.objects.all()    
    # Filter selected users based on their IDs
    selected_users = []
    for user_id in selected_ids:
        print(f">>>>> {user_id}")
        user = get_object_or_404(all_users, pk=user_id)
        selected_users.append(user)
    print(f">>>>> selected users {selected_users}")
    return selected_users

######################################### group mgmt ##########################################
@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def group_home(request):
    context = {'page': 'Group Home'}
    return render(request, 'role_based_templates/group_mgmt/group_mgmt_home.html', context)



@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def group_list(request):
    query = ''
    group_object=CustomGroup
    groups = group_object.objects.filter(active=True).order_by('name')
    
     # pagination
    pagination_on = False
    selected_pagination = request.GET.get('pagination', 'all')
    #selected_pagination = 'all'
    if selected_pagination == 'all':
        paginated_items = groups
        pagination_on = False
    else:
        pagination_on = True
        items_per_page = int(selected_pagination) 
        paginator = Paginator(groups, items_per_page)        

        page_number = request.GET.get('page')
        try:
            paginated_items = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_items = paginator.page(1)
        except EmptyPage:
            paginated_items = paginator.page(paginator.num_pages)
    
    context = {'page': 'User List', 'active_tab': 'list_groups', 
                   'groups': groups, 'query': query,
                   'pagination':selected_pagination, 
                   'paginated_items': paginated_items, 'pagination_on': pagination_on}

    if request.method == 'POST':
        query = request.POST.get('q')
        if query:
            #users = User.objects.filter(username__icontains=query)
            groups = group_object.objects.filter(
                    Q(name__icontains=query) )
        else:
            groups = group_object.objects.all()
        if query is None:
            query = ''
        # pagination
        pagination_on = False
        selected_pagination = request.GET.get('pagination', 'all')
        #selected_pagination = 'all'
        if selected_pagination == 'all':
            paginated_items = groups
            pagination_on = False
        else:
            pagination_on = True
            items_per_page = int(selected_pagination) 
            paginator = Paginator(groups, items_per_page)        

            page_number = request.GET.get('page')
            try:
                paginated_items = paginator.page(page_number)
            except PageNotAnInteger:
                paginated_items = paginator.page(1)
            except EmptyPage:
                paginated_items = paginator.page(paginator.num_pages)
        
        context = {'page': 'Group List', 'active_tab': 'group_mgmt_list', 
                    'groups': groups, 'query': query,
                    'pagination':selected_pagination, 
                    'paginated_items': paginated_items, 'pagination_on': pagination_on}
       
        return render(request, 'role_based_templates/group_mgmt/group_mgmt_list.html', context)
    else:
        return render(request, 'role_based_templates/group_mgmt/group_mgmt_list.html', context)


@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def group_create(request):
    context = {'page': 'Group Add', 'active_tab': "add_group"}
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_mgmt_list') 
    else:
        form = GroupForm()
    context = {
        'active_tab': "add_group",
        'form': form,
    }
    return render(request, 'role_based_templates/group_mgmt/group_mgmt_add.html', context)

@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def group_delete(request, pk):
    context = {'page': 'Group Home'}
    group_object=CustomGroup
    group = get_object_or_404(group_object, pk=pk)
    if request.method == 'POST':
        form = DeleteGroupConfirmationForm(request.POST)
        if form.is_valid():
            #group.delete()
            group_object.objects.filter(id=pk).update(active=False)
            return redirect('group_mgmt_list') 
    else:
        form = DeleteGroupConfirmationForm()
    context = {
        'active_tab': 'delete_group',
        'delete_group': group,
    }
    return render(request, 'role_based_templates/group_mgmt/group_mgmt_confirm_delete.html', context)

@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def group_update(request, pk):
    context = {'page': 'Group Home'}
    group_object=CustomGroup
    form = GroupForm()
    list = get_object_or_404(group_object, id=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=list)
        if form.is_valid():
            form.save()
            return redirect('group_mgmt_list') 
    else:
        form = GroupForm(instance=list)
    context = {
        'active_tab': 'update_group',
        'form': form,
    }
    return render(request, 'role_based_templates/group_mgmt/group_mgmt_update.html', context)

@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def group_detail(request,pk):
    group_object=CustomGroup
    context = {'page': 'Group Details'}
    group = get_object_or_404(group_object, pk=pk)
    context = {'group':group, 'active_tab':'group_details'}
    return render(request, 'role_based_templates/group_mgmt/group_mgmt_details.html', context)

# 
@login_required(login_url='login')
@check_site_permissions_type('site_admin')
def group_mgmt_list_users(request,pk):
    group_object=CustomGroup
    context = {'page': 'Group Details'}
    group = get_object_or_404(group_object, pk=pk)
    users_in_group = User.objects.filter(groups=group)
    context = {'group':group, 'active_tab':'group_details', 'users_in_group': users_in_group}
    return render(request, 'role_based_templates/group_mgmt/group_mgmt_list_users.html', context)

