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
from ..decorators import *
from app_baseline.models.delivery import *
from app_baseline.models.user.model_user import *
# Create your views here.
# ops of the planner

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


######################################## Begin Generic Object CRUD ############################
@login_required(login_url='login')
@check_site_permissions_type('site_edit')
def add_object(request, model_name):
    model_class = None
    model_class = get_model_class(model_name)
    if model_class is not None:
        print(f">>> === {model_name} === <<<")
        if request.method == 'POST':
            # Here, we use the relevant form for the model
            form = globals()[model_name + 'Form'](request.POST)
            print(f">>>>>>>>>>>>>"+ str(form.errors))
            if form.is_valid():
                form.instance.author = request.user
                obj = form.save()
                print(f">>>>>>>>>>>>>>>>>>>>> MODEL NAME: {model_name}")
                # Handle any specific logic for creating related objects
                if model_name in ['Product', 'Project', 'Service', 'Solution', 'ValueStream', 'Organization', 'Team']:
                    work_item_type = form.cleaned_data['work_item_type']
                    print(f">>>>>>>>>>>>>>>>>>> {work_item_type}")
                    obj_work_item_type = None
                    lc_model_name = model_name.lower()
                    print(f"=================================== IMP >>>> {lc_model_name} {obj.id} {obj} ")
                    # Create a related Backlog entry only if it doesn't exist
                    backlog_title = f"{obj.title} Backlog"
                    backlog = CORE_HSDB.objects.create(
                        title=backlog_title,
                        **{lc_model_name: obj},
                        active=True,
                        author=request.user,
                        #workitemtype=obj_work_item_type,
                    )
                    vmvsri = f"{obj.title} VMV"
                    backlog = VisionMissionValueSRI.objects.create(
                        title=backlog_title,
                        **{lc_model_name: obj},
                        active=True,
                        author=request.user,
                        #workitemtype=obj_work_item_type,
                    )
                    ##
                    ## Basic Value => Group creation
                    ##
                    value_view_identifier = f"{model_name}_{obj.id}_view"
                    value_edit_identifier = f"{model_name}_{obj.id}_edit"
                    value_admin_identifier = f"{model_name}_{obj.id}_admin"
                    groupe = CustomGroup.objects.create(name=value_view_identifier,active=True,author=request.user,)
                    groupv = CustomGroup.objects.create(name=value_edit_identifier,active=True,author=request.user,)
                    groupa = CustomGroup.objects.create(name=value_admin_identifier,active=True,author=request.user,)
                    owner_of_group = User.objects.filter(username=request.user).first()
                    owner_of_group.groups.add(groupa)
                # Handle form submission success
                return redirect('kanban_home')
        else:
            # Here, we use the relevant form for the model
            form = globals()[model_name + 'Form']()

        context = {'page': 'Add ' + model_name, 'form': form, 'value_type': model_name}
        template_name = 'app_xpresskanban/create_value.html'
        print(f">>>>>>>>>>>>>>>>>>>>>> {template_name}")
        return render(request, template_name, context)
    else:
        # Handle invalid model name
        return redirect('home')  # Redirect to a proper error page or other handling

# def get_object_ref(model, name):
#     object_ref = get_object_or_404(model, title=name)
#     return object_ref
def get_object_ref(model_class, identifier):
    try:
        obj = model_class.objects.get(title=identifier)  # Replace identifier_field with the actual field name
        return obj
    except model_class.DoesNotExist:
        return None
@login_required(login_url='login')
@check_value_permissions_type('edit')
def create_charter(request, value_type, pk):
    model_name = value_type
    model_class = get_model_class(model_name)
    obj = get_object_or_404(model_class, pk=pk)
    lc_model_class = model_name.lower()
    val_lookup = {lc_model_class: obj}
    url_ref = reverse('value_homepage', args=[model_name, pk])
    
    # Check if entry exists in VisionMissionValueSRI
    vmvsri, created = VisionMissionValueSRI.objects.get_or_create(**val_lookup)
    
    if request.method == 'POST':
        form = VMVSRIForm(request.POST, instance=vmvsri)
        
        if form.is_valid():
            form.instance.title = "Testing"
            setattr(form.instance, value_type.lower(), obj)
            form.instance.author = request.user
            form.save()
            print(f">>>>>>>>>>>>>>>>>>>>> FORM SAVE CHARTER MODEL NAME: {model_name}")
            return redirect(url_ref)
        else:
            print(f"Form Errors: {form.errors}")
    else:
        form = VMVSRIForm(instance=vmvsri)
    
    context = {'form': form, model_name: obj, 'object': obj, 'value_type': value_type}
    return render(request, 'app_xpresskanban/create_charter.html', context)

@login_required(login_url='login')
@check_value_permissions_type('view')
def view_value(request, value_type, pk):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)

    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        context = {model_name: obj, 'object': obj, 'value_type': value_type}
        return render(request, 'app_xpresskanban/view_value.html', context)
    else:
        # Handle invalid model name
        return redirect('home')  # Redirect to a proper error page or other handling

@login_required(login_url='login')
@check_value_permissions_type('edit')
def edit_value(request, value_type, pk):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)

    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        form = globals()[model_name + 'Form'](instance=obj)
        if request.method == 'POST':
            form = globals()[model_name + 'Form'](request.POST, instance=obj)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect('/kanban/list_values/'+model_name)
            else:
                print(f">>>>> FORM IS INVALID: {form}")
        else:
            form = globals()[model_name + 'Form'](instance=obj)
        context = {'page': 'Edit ' + model_name,'form': form, model_name: obj
                   ,'value_type': value_type, 'object': obj}
        return render(request, 
                      'app_xpresskanban/edit_value.html', context)
    else:
        # Handle invalid model name
        return redirect('kanban_home')  # Redirect to a proper error page or other handling

@login_required(login_url='login')
@check_value_permissions_type('edit')
def delete_value(request, value_type, pk):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    url_ref = reverse('list_values', args=[model_name])
    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        context = {model_name: obj, 'object': obj}
        if request.method == 'POST':
            model_class.objects.filter(id=pk).update(active=False, author=request.user)     
            return redirect(url_ref)
        return render(request, 'app_xpresskanban/delete_object_confirm.html', context)
    else:
        # Handle invalid model name
        return redirect('kanban_home')  # Redirect to a proper error page or other handling

# Add other views like "copy_object", "restore_object", etc. following the same pattern
################################################# NEW DEFINITION ###########################
@login_required(login_url='login')
@user_in_group(['View_Value_Group'])
def list_values(request, value_type):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    print(f">>> === {value_type} === <<<")
    if model_class is not None:
        context = {'page': model_class}        
        # here we list all values
        newtodolist = model_class.objects.filter(active=True).order_by('position')
        print(f">>> === {newtodolist} === <<<")
        newtodolist_count = newtodolist.count()
        form = globals()[model_name + 'Form'](request.POST)
        # pagination
        pagination_on = False
        selected_pagination = request.GET.get('pagination', 'all')
        #selected_pagination = 'all'
        if selected_pagination == 'all':
            paginated_items = newtodolist
            pagination_on = False
        else:
            pagination_on = True
            items_per_page = int(selected_pagination) 
            paginator = Paginator(newtodolist, items_per_page)        

            page_number = request.GET.get('page')
            try:
                paginated_items = paginator.page(page_number)
            except PageNotAnInteger:
                paginated_items = paginator.page(1)
            except EmptyPage:
                paginated_items = paginator.page(paginator.num_pages)
    
    context = {'newtodolist': newtodolist,'form':form, 'newtodolist_count': newtodolist_count, 
               'pagination':selected_pagination, 'paginated_items': paginated_items, 
               'pagination_on': pagination_on, 'value_type': value_type}
    return render(request, 'app_xpresskanban/list_values.html', context)


@login_required(login_url='login')
@check_value_permissions_type('edit')
def manage_value(request, value_type, pk):
    context = {'page': 'Manage Value', 'active_tab': 'manage_value',
               'value_type': value_type, 'pk':pk}
    return render(request, 'app_xpresskanban/list_values.html', context)

@login_required(login_url='login')
def sorted_value(request, value_type):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    if model_class is not None:
        context = {'page': model_class}        
        if request.method == 'POST':
            ajax_data = request.POST['sorted_list_data']
            print(f">>>>> AJAX DATA : {ajax_data}")
            new_data = ajax_data.replace("[",'')
            new_data = new_data.replace("]",'')
            sorted_list = new_data.split(",")
            print(f">>>>> AJAX DATA : {sorted_list}")
            seq = 1
            for item in sorted_list:
                str = item.replace('"','')
                position = str.split('_')
                model_class.objects.filter(pk=position[0]).update(position=seq)
                seq = seq + 1

    context = {'page': 'Sorted Value', 'active_tab': 'sorted_value',
               'value_type': value_type, }
    return render(request, 'app_xpresskanban/list_values.html', context)


### bulk operations ###
@login_required(login_url='login')
@check_site_permissions_type('edit')
def bulk_restore_deleted_values(request, value_type):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    if model_class is not None:
        if request.method == 'POST':
            form_data = request.POST
            selected_project_ids = request.POST.getlist('restore_project_box')        
            bulk_ops = form_data.get('bulk_project_ops')
            if bulk_ops == "bulk_restore":
                for id in selected_project_ids:
                    model_class.objects.filter(id=id).update(active=True,  author=request.user)
            elif bulk_ops == "bulk_not_done":
                for id in selected_project_ids:
                    model_class.objects.filter(id=id).update(done=False,  author=request.user)
            elif bulk_ops == "bulk_delete_permanently":
                for id in selected_project_ids:
                    model_class.objects.filter(id=id).update(active=False, deleted=True,  author=request.user)
            pagination = form_data.get('pagination')
            print(f">>>>>>>>>>>.FORM. {bulk_ops} is bulk_ops, pagination {pagination}")
            context = {'bulk_ops': bulk_ops, 'pagination': pagination, 
                    'selected_project_ids':selected_project_ids, 'value_type': value_type}
        return render(request, 'app_xpresskanban/bulk_restore_ops_value.html', context)


# restore: listing the values that needs to be restored
@login_required(login_url='login')
@check_value_permissions_type('edit')
def restore_value(request, value_type, pk):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        context = {'object': obj}
        url_ref = reverse('restore_values', args=[model_name])
        if request.method == 'POST':
            model_class.objects.filter(id=pk).update(active=True,  author=request.user)
            return redirect(url_ref)
        return render(request, 'app_xpresskanban/restore_value.html', context)
@login_required(login_url='login')
@check_site_permissions_type('edit')
def restore_values(request, value_type):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    if model_class is not None:
        context = {'page': 'Restore Values'}
        # here we list all projects deleted and restore
        newtodolist = model_class.objects.filter(active=False, deleted=False).order_by('position')
        newtodolist_count = newtodolist.count()
        form = globals()[model_name + 'Form'](request.user)
        url_ref = reverse('list_values', args=[model_name])
        if request.method == 'POST':
            form = globals()[model_name + 'Form'](request.user, request.POST)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                todo_count = newtodolist.count()
                return redirect(url_ref)
            else:
                print(f"form is invalid {form}")
        context = {'newtodolist': newtodolist,'form':form, 
                   'newtodolist_count': newtodolist_count, 'value_type': value_type}
        return render(request, 'app_xpresskanban/restore_values.html', context)


# ops_project ==> ops_value
@login_required(login_url='login')
@check_site_permissions_type('edit')
def ops_value(request, value_type):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    if model_class is not None:
        if request.method == 'POST':
            form_data = request.POST
            selected_project_ids = request.POST.getlist('project_box')        
            bulk_ops = form_data.get('bulk_project_ops')
            pagination = form_data.get('pagination')
            bulk_ops = form_data.get('bulk_project_ops')
            if bulk_ops == "bulk_delete":
                for id in selected_project_ids:
                    model_class.objects.filter(id=id).update(active=False, deleted=False,  author=request.user)
            elif bulk_ops == "bulk_done":
                for id in selected_project_ids:
                    model_class.objects.filter(id=id).update(done=True,  author=request.user)
            print(f">>>>>>>>>>>.FORM. {bulk_ops} is bulk_ops, pagination {pagination}")
            context = {'bulk_ops': bulk_ops, 'pagination': pagination, 
                       'selected_project_ids':selected_project_ids,
                       'value_type': value_type}
            return render(request, 'app_xpresskanban/bulk_value_ops.html', context)


# copy value

@login_required(login_url='login')
@check_value_permissions_type('edit')
def copy_value(request, value_type, pk):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    if model_class is not None:
        object = get_object_or_404(model_class, pk=pk)
        new_project = model_class()
        new_project.title = object.title + " (Copy)"
        new_project.description = object.description
        new_project.type = object.type
        new_project.priority = object.priority
        new_project.state = object.state
        new_project.start_date = object.start_date
        new_project.end_date = object.end_date
        new_project.current_state = object.current_state
        new_project.work_item_type = object.work_item_type
        new_project.save()
        new_project_id = new_project.id
        lc_model_name = model_name.lower() 
        #######################################
        # Create a related Backlog entry only if it doesn't exist
        backlog_title = f"{new_project.title} Backlog"
        backlog = CORE_HSDB.objects.create(title=backlog_title, 
                   **{lc_model_name: new_project}, active=True, author=request.user,
                    workitemtype=object.work_item_type)
        context = {'object': object, 'new_project_id':new_project_id, 
                'new_project':new_project, 'backlog': backlog, 'value_type': value_type}
        return render(request, 'app_xpresskanban/copy_value.html', context)

from django.template import Template, Context
from markdownx.utils import markdownify
@login_required(login_url='login')
@check_value_permissions_type('view')
def value_homepage(request, value_type, pk):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    
    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        lc_model_class = model_name.lower()
        val_lookup = {lc_model_class: obj}
        vision = VisionMissionValueSRI.objects.get(**val_lookup)
        template = Template(vision.vision)
        rendered_markdown = template.render(Context(template))
        context = {model_name: obj, 'object': obj, 'value_type': value_type, 
                   'vision': vision, 'rendered_markdown':rendered_markdown}
        return render(request, 'app_xpresskanban/value_homepage.html', context)
