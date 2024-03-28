# all imports
from ..all_view_imports import *

# config
from ..._common.config.config import *

# specific imports
from ...forms.user.form_user import *
from ...forms.list.form_list import *
from ...forms.permission.form_permission import *
from ...models.user.model_user import *
from ...models.list.model_list import *

from ...decorators.authz.decorator_authorization import *
from ...decorators.authz.decoraton_v1_authz import *
from app_web.models import *
# which app is being referred
app_base_ref = base_app_ref
my_wbs = ["Strategic Theme", "Epic", "Feature", "Capability", "Component", "Spike", "User Story", "Task", ]
parent_wbs = ["Epic", "Feature", "Capability", "Component", "Spike", "User Story",  ]

@login_required(login_url='login')
def permission_settings(request, list_id):
    object = List.objects.get(id=list_id)
    logger.debug(f">>> === {object}=== <<<")
    permission_id = object.permission.id
    permission = Permission.objects.get(id=permission_id)
    if request.method == 'POST':
        post_data = request.POST.copy()
        users = post_data.getlist('users')
        if '' in users:
            users.remove('')
        post_data.setlist('users', users)
        form = PermissionForm(post_data, instance=permission)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            logger.debug(f">>> === {form.cleaned_data}=== <<<")     
            permission = form.save()
            # Usage
            node = List.objects.get(id=list_id)  # Replace with your actual model and node id
            return redirect('list_home')
    else:
        form = PermissionForm(instance=permission)
    context = {'form': form}
    template_url = f"{app_base_ref}/jstree_templates/jstree_common/permission_settings.html"
    return render(request, template_url, context )


# Edit
@login_required(login_url='login')
def edit_permission(request, permission_id):
    instance = ListPermission.objects.get(id=permission_id)
    form = ListPermissionForm(request.POST or None, instance=instance)
    url = reverse('list_js_tree_id', args=[instance.list_node.id])
    if form.is_valid():
        form.save()
        return redirect(url)  # Redirect to list view or wherever appropriate
    context = {'form': form}

    template_url = f"{app_base_ref}/jstree_templates/jstree_common/edit_permission.html"
    return render(request, template_url, context )


# Delete
@login_required(login_url='login')
def delete_permission(request, permission_id):
    instance = ListPermission.objects.get(id=permission_id)
    instance.active = False
    instance.save()
    url = reverse('list_js_tree_id', args=[instance.list_node.id])
    return redirect(url)  # Redirect to list view or wherever appropriate


@login_required(login_url='login')
def test_method(request, list_id):
    if request.method == 'POST':
        print(request.POST)
        
        template_url = f"{app_base_ref}/jstree_templates/jstree_common/test_method.html"
        context = {'list_id': list_id}
        return render(request, template_url, context )


@login_required(login_url='login')
def ajax_user_suggest(request):
    query = request.GET.get('term', '')
    users = User.objects.filter(username__icontains=query)
    suggestions = [{'label': user.username, 'id': user.id} for user in users]
    return JsonResponse(suggestions, safe=False)


# def get_permitted_nodes_for_user(request, queryset):
#     user = request.user

#     permitted_nodes = queryset.filter(user=user)  # Start with nodes owned by the user
#     public_nodes = queryset.filter(listpermission__users_can_view=True, listpermission__active=True)
#     permitted_nodes = (permitted_nodes | public_nodes).distinct()
#     for obj in queryset:
#         list_permissions = obj.listpermission_set.all()  # Replace with the correct related_name or default set
#         for lp in list_permissions:
#             print(f"===> {lp.list_node} active {lp.active} ==> {lp.users_can_view}")
#     return permitted_nodes

# def get_permitted_nodes_for_user(request, queryset):
#     user = request.user
    
#     # Nodes created by the user
#     user_created_nodes_query = Q(user=user)
    
#     # Nodes that are viewable by everyone
#     public_viewable_nodes_query = Q(listpermission__users_can_view=True)
    
#     # Combined user-created and publicly viewable nodes query
#     combined_nodes_query = user_created_nodes_query | public_viewable_nodes_query
    
#     # Query to get permissions set explicitly for the user
#     user_permissions_query = Q(listpermission__users__in=[user])

#     # Query to get permissions set for groups that the user belongs to
#     user_groups = user.groups.all()
#     group_permissions_query = Q(listpermission__groups__in=user_groups)

#     # Combine the queries
#     combined_permissions_query = user_permissions_query | group_permissions_query

#     # Combine all the queries
#     final_combined_query = combined_nodes_query | combined_permissions_query
    
#     final_permitted_nodes = queryset.filter(
#         final_combined_query,
#         listpermission__can_view=True
#     ).distinct()

#     return final_permitted_nodes

def get_permitted_nodes_for_user(request, queryset):
    user = request.user
    user_groups = user.groups.all()
    user_list = queryset.filter(user=user)  # Start with nodes owned by the user
    general_list = queryset.filter(listpermission__users_can_view=True, listpermission__active=True)
    
    
    # Nodes where the user has explicit 'can_view' permission
    user_explicit_permission = queryset.filter(
        listpermission__users__in=[user],
        listpermission__can_view=True,
        listpermission__active=True,
        active=True,
    )
     # Nodes where the user's groups have 'can_view' permission
    group_explicit_permission = queryset.filter(
        listpermission__groups__in=user_groups,
        listpermission__can_view=True,
        listpermission__active=True,
        active=True,
    )
    
    permitted_nodes = (user_list | general_list | user_explicit_permission | group_explicit_permission).distinct()
    return permitted_nodes


@login_required(login_url='login')
def list_home(request):
    objects = List.objects.filter(parent=None, active=True, deleted=False).order_by('position', 'created_at')
    objects_count = objects.count()
    context = {'page': 'list_home', }
    form = ListForm(request)
    if request.method == 'POST':
        objects = List.objects.filter(parent=None, active=True, deleted=False).order_by('position', 'created_at')
        objects_count = objects.count()
        form = ListForm(request.user, data=request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.parent = None
            form.save()
            context['objects'] = objects
            # *** setup permissions ***
            new_list_id = form.instance.id
            ref_type_id = form.instance.type
            # *** end setup permissions ***
        else:
             context['error'] = "Form is Invalid"
    
    permitted_nodes = get_permitted_nodes_for_user(request, objects)
    objects = permitted_nodes
    objects_count = permitted_nodes.count()
    context = {'page': 'list_home', 'objects': objects, 'objects_count': objects_count,
               'form': form,}
    template_url = f"{app_base_ref}/basics/list/list_home.html"
    return render(request, template_url, context)

@login_required(login_url='login')
def delete_list_item(request, list_id):    
    context = {'page': 'list_home', }
    object = List.objects.filter(id=list_id).update(active=False)
    parent=get_object_or_404(List, id=list_id).parent
    template_url = f"{app_base_ref}/basics/list/list_home.html"       
    objects = List.objects.filter(user=request.user, active=True, deleted=False).order_by('position','created_at')
    context = {'page': 'list_home', 'objects': objects}
    if request.GET.get('list_item') != None and request.GET.get('list_item') == 'yes':
        return redirect("list_items", list_id=parent.id)
    return redirect("list_home")

# 
#  List children
#
@login_required(login_url='login')
def list_items(request, list_id):   
    request.permitted_nodes = None
    context = {'page': 'list_home', }
    parent = get_object_or_404(List, pk=list_id)
    children = None
    ancestors = None
    get_last_item = None
    if not parent.is_leaf_node():
        children = parent.get_children()    
    # iterate through children and get their parents
    if children:
        #print(f" CHILDREN PRESENT {children}")
        children_present=True
    else:
        ancestors = parent.get_ancestors()
    if children != None:
        for child in children:
            ancestors = child.get_ancestors()
            if ancestors:
                parent = ancestors[0]
                imm_parent = ancestors.reverse()[0]
            else:
                logger.debug(f">>> === {child} has no parent === <<<")
    objects = List.objects.filter(parent_id=list_id, active=True).order_by('position')
    objects_count = objects.count()
    if objects_count == 0:
        get_last_item = List.objects.get(id=list_id)
    # post method processing
    list = ListForm(request.user, current_parent_id=list_id)
    if request.method == 'POST':
        list = ListForm(request.user, current_parent_id=list_id, data=request.POST)
        if list.is_valid():
            parent = list.cleaned_data['parent']
            list = list.save(commit=False)
            list.parent = parent
            list.user = request.user
            list.save()
            #print(f">>> === List Item {list} === <<<")
        list = ListForm(request.user, current_parent_id=list_id, )
        objects = List.objects.filter(parent_id=list_id, active=True).order_by('position')
        objects_count = objects.count()

    permitted_nodes = get_permitted_nodes_for_user(request, objects)
    objects = permitted_nodes
    objects_count = permitted_nodes.count()
    context = {'page': 'list_home', 'objects': objects, 'objects_count': objects_count,
               'parent_id': list_id, 'last_item': get_last_item,
               'ancestors':ancestors,'form':list,
               }
    template_url = f"{app_base_ref}/basics/list/list_items.html"
    return render(request, template_url, context)
#######################################################################################
# copy and deep-copy / clone

@login_required(login_url='login')
def clone_list_items(request, list_id):
    node = List.objects.get(id=list_id)
    clone_node = List.objects.create(title=node.title, type=node.type, parent=node.parent, user=request.user)
    #print(f"CLONE node: {clone_node}")
    url = None
    if request.GET.get('list') != None and request.GET.get('list') == "yes":
        url = reverse('list_home')
    else:
        url = reverse('list_items', args=[node.parent.id])
    return redirect(url)

@login_required(login_url='login')
def deep_clone_list_items(request, list_id):
    node = List.objects.get(id=list_id)
    descendants = node.get_descendants(include_self=True)
    clone_node = List.objects.create(title=node.title + " (cloned) ", parent=node.parent, 
                                            type=node.type,
                                            description=node.description,
                                            user=request.user)
    #print(f">>> STEP1: node {node.id} {node} is cloned as {clone_node.id} {clone_node.id} ")

    # =============== STEP2 =================
    map_nodes = {}
    for descendant in node.get_descendants().filter(active=True):
        step2_flag = True
        #print(f">>> STEP2: Map nodes {descendant.parent.id}|{descendant.id}")
        if descendant.parent.id in map_nodes:
            map_nodes[descendant.parent.id].update({descendant.id: descendant.title})
        else:
            map_nodes[descendant.parent.id] = {descendant.id: descendant.title}

    # =============== STEP3 =================
    backup_nodes = map_nodes
    #print(f">>> STEP3: Cloned Node takes place {map_nodes} and backup nodes {backup_nodes}")
    map_nodes[clone_node.id] = map_nodes[node.id]
    del map_nodes[node.id]
    #print(f">>> STEP4: Move to cloned node {map_nodes}")
    if clone_node.id in map_nodes:
        for k,v in map_nodes[clone_node.id].items():
            test2 = List.objects.get(id=k)
            ic = List.objects.create(title=v, parent_id=clone_node.id, 
                                            description=test2.description,
                                            user=request.user)
            # recurse from here
            # recurse_clone_from_map(k, ic.id, map_nodes)
            recurse_clone_from_map(k, ic, map_nodes, List, request)
            #print(f"IMMEDIATE CLONE {node.id}, {node}: {ic.parent.id}, {ic.parent}, {ic.id}")
        del map_nodes[clone_node.id]
    #print(f"CLONE_NODE {clone_node.id} from NODE {node.id}")
    #print(f"MAP NODES after cloning: {map_nodes}")
    url = None
    if request.GET.get('list') != None and request.GET.get('list') == "yes":
        url = reverse('list_home')
    else:
        url = reverse('list_items', args=[node.parent.id])
    return redirect(url)

def recurse_clone_from_map(k, ic, map_nodes, mainobject, request):
    if k in map_nodes:
        #print(f" RECURSE ******* {k}")
        for k1,v1 in map_nodes[k].items():
            test3 = List.objects.get(id=k1)
            iic = mainobject.objects.create(title=v1, parent_id=ic.id, 
                                            description=test3.description,
                                            user=request.user)
            if k1 in map_nodes:
                #print(f" ******* >>>>> TEST {k1}")
                recurse_clone_from_map(k1, iic, map_nodes, mainobject, request)
    return map

@login_required(login_url='login')
def edit_list(request, list_id):
    form = EditListForm(request.user, current_parent_id=list_id)
    object = None
    parent = None
    try:
        object = List.objects.get(id=list_id)
        parent = object.parent
        form = EditListForm(request.user, current_parent_id=list_id, instance=object)
    except:
        print(f"EDIT TODOLIST TOPIC>>> TOPIC {list_id}  not found.")
        messages.error(request, f"Edit: TOPIC {list_id}  not found.")
    if request.method == 'POST':
        form = EditListForm(request.user, current_parent_id=list_id, data=request.POST or None,  instance=object,)
        if form.is_valid():
            form.save()
            if parent  != None:
                if object.parent != None:
                    url = reverse('list_items', args=[object.parent.id])
                    return redirect(url)
            else:
                return redirect('list_home')
                
            return redirect('list_home')

    context = {'form': form}
    template_url = f"{app_base_ref}/basics/list/edit_list.html"
    return render(request, template_url, context)
 

#######################################################################################
#
# AJAX related: List top level
#
@login_required(login_url='login')
def ajax_update_list_item(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')
        title = request.POST.get('title')
        done = request.POST.get('done')   
        save_field_done = False
        if done == "true":
            save_field_done=True
        #print(f">>> === AJAX UPDATE LIST ITEM {title} === <<<")
        
        try:            
            object = List.objects.get(id=object_id)
            # Update the fields
            object.title = title
            object.done = save_field_done
            object.save()
            print(f">>> === (saved) AJAX UPDATE LIST ITEM {title} === <<<")
            # end of card movement update
            return JsonResponse({'success': True})
        except List.DoesNotExist:
            pass
    
    return JsonResponse({'success': False})



@login_required(login_url='login')
def ajax_rename_list_item(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')
        title = request.POST.get('title')
        print(f">>> === AJAX RENAME LIST ITEM {title} {object_id} === <<<")
        
        try:            
            object = List.objects.get(id=object_id)
            # Update the fields
            object.title = title
            object.save()

            # end of card movement update
            return JsonResponse({'success': True})
        except List.DoesNotExist:
            pass
    
    return JsonResponse({'success': False})

@login_required(login_url='login')
def ajax_update_list_sorted(request):
    if request.method == 'POST':
        ajax_data = request.POST['sorted_list_data']
        new_data = ajax_data.replace("[",'')
        new_data = new_data.replace("]",'')
        sorted_list = new_data.split(",")
        seq = 1
        print(f">>> === AJAX UPDATE SORTED === <<<")
        for item in sorted_list:
            str = item.replace('"','')
            position = str.split('_')
            print(f">>> === AJAX UPDATE SORTED {position} === <<<")
            List.objects.filter(pk=position[0]).update(position=seq)
            seq = seq + 1
        context = {'page': 'Sorted Value', 
                   'active_tab': 'sorted_value',
                   'ajax_data': ajax_data}
        return JsonResponse({'success': True})
    
######################################################################################
# experiment jstree
@login_required(login_url='login')
def ajax_get_type_details(request):
    if request.method == 'POST':
        object_id = request.POST.get('node_id')
        object = List.objects.get(id=object_id)
        object_type = object.type
        type = Type.objects.get(id=object_type.id)
        got_types = type.children()
        send_types = []
        for each_type in got_types:
            send_types.append(each_type.title)
        #serialized_types = serialize('json', send_types)
        print(f">>> === NODE: {object} {object_id}, TYPE: {object_type} {object_type.id} ==> {send_types} === <<<")
        details = {
            'types': send_types,
            # Add other details
        }
        return JsonResponse(details)
@login_required(login_url='login')
def ajax_get_tree_data(request):
    root_nodes = List.objects.filter(user=request.user, parent=None, active=True, deleted=False).order_by('position', '-created_at')
    data = []
    
    def add_node_and_children(node):
        level = node.level  # Assuming nodes have a level attribute
        is_opened = level < 2  # Open up to level 2 (0-indexed)
        if level < 2:
            is_opened = "true"
        #print(f">>> === **** LEVEL {level}:{is_opened} **** === <<<")
        
        parent = node.parent.id if node.parent else '#'
        #print(f">>> === **** NODE TYPE: {node.type} **** === <<<")
        type_icon = "default"
        type_detail = None
        if node.type != None and node.active == True:
            type_icon = node.type.title
            type_icon = type_icon.lower()
            type_icon = type_icon.strip()
            child_nodes_details = []
            for child in node.type.children():  # Replace children() with your method to get child nodes
                child_details = {
                    'id': child.id,
                    'title': child.title
                    # Add more fields here if needed
                }
                child_nodes_details.append(child_details)
            type_detail = {
            'type_id': node.type.id,
            'type_title': node.type.title,
            'child_nodes': child_nodes_details,  # Replace get_children() with your method to get child nodes
            }
            
        node_data = {'id': str(node.id), 'parent': str(parent), "type": type_icon, 'text': node.title, 'state': {'opened': is_opened}}
        if type_detail:
            node_data['type_details'] = type_detail
        
        data.append(node_data)

        for child in node.get_children():
            if child.active == True:
                add_node_and_children(child)
                # edge case node char length to be specific to avoid overlap on div

    for root in root_nodes:
        add_node_and_children(root)

    response_data = {
        'data': data,
    }
    #print(f">>> === {response_data} === <<<")
    return JsonResponse(response_data, safe=False)

@login_required(login_url='login')
def ajax_get_tree_data_id(request):
    if request.method == 'POST':
        list_id = request.POST.get('list_id')
        root_nodes = List.objects.filter(id=list_id, active=True, deleted=False).order_by('position', '-created_at')
        data = []
        
        def add_node_and_children(node):
            level = node.level  # Assuming nodes have a level attribute
            is_opened = level < 2  # Open up to level 2 (0-indexed)
            if level < 2:
                is_opened = "true"
            #print(f">>> === **** LEVEL {level}:{is_opened} **** === <<<")
            
            if node.id == list_id:
                parent = "#"
            else:
                parent = node.parent.id if node.parent else '#'
            logger.debug(f">>> === **** NODE TYPE: {node.type} **** === <<<")
            type_icon = "default"
            type_detail = None
            if node.type != None and node.active == True:
                type_icon = node.type.title
                type_icon = type_icon.lower()
                type_icon = type_icon.strip()
                child_nodes_details = []
                for child in node.type.children():  # Replace children() with your method to get child nodes
                    child_details = {
                        'id': child.id,
                        'title': child.title
                        # Add more fields here if needed
                    }
                    child_nodes_details.append(child_details)
                type_detail = {
                'type_id': node.type.id,
                'type_title': node.type.title,
                'child_nodes': child_nodes_details,  # Replace get_children() with your method to get child nodes
                }
            
            node_data = {'id': str(node.id), 'parent': str(parent), "type": type_icon, 'text': node.title, 'state': {'opened': is_opened}}
            if type_detail:
                node_data['type_details'] = type_detail
            
            data.append(node_data)

            for child in node.get_children():
                if child.active == True:
                    add_node_and_children(child)
                    # edge case node char length to be specific to avoid overlap on div

        for root in root_nodes:
            add_node_and_children(root)


      
        response_data = {
            'data': data,
        }
        #print(f">>> === {response_data} === <<<")
        return JsonResponse(response_data, safe=False)

@login_required(login_url='login')
def ajax_get_node_details(request):
    if request.method == 'POST':
        list_id = request.POST.get('node_id')
        object = List.objects.get(id=list_id)
        parent_title = ""
        description = "TESTING"
        if object.parent != None:
            parent_title = object.parent.title
        details = {
            'parent': parent_title,
            'title': object.title,
            'description': description,
            'created_at': object.created_at,
            'updated_at': object.updated_at,
            # Add other details
        }
        return JsonResponse(details)
    

@login_required(login_url='login')
def ajax_save_list_permission(request):

    # First, get the 'formData' value from the QueryDict
    form_data_string = request.POST.get('formData')

    # Next, parse the string to extract 'list_node_id'
    form_data_list = form_data_string.split('&')
    list_node_id = None
    for item in form_data_list:
        if 'list_node_id' in item:
            list_node_id = item.split('=')[1]
            break
    list_id = list_node_id
    form_data = {}
    for item in form_data_list:
        key, value = item.split('=')
        form_data[key] = value

    form_data['list_node_id'] = list_node_id
    form = ListPermissionForm(form_data)

    list_node = List.objects.get(id=list_id)

    list_permission = ListPermission.objects.filter(active=True, list_node=list_node_id)

    if request.method == 'POST':
        serialized_form_data = request.POST.get('formData', '')
        form_data = QueryDict(serialized_form_data)

        form = ListPermissionForm(form_data)
        #print(f">>> === |||||||||||||||||||||||| {form_data} ||||||||||||||| === <<<")
        if form.is_valid():
            instance = form.save(commit=False)
            instance.list_node = list_node

            # Default settings when delete is ticked
            if form.cleaned_data.get('can_delete', False):
                instance.can_view = True
                instance.can_add = True
                instance.can_change = True
            if form.cleaned_data.get('can_change', False):
                instance.can_view = True
                instance.can_add = True
            if form.cleaned_data.get('can_add', False):
                instance.can_view = True

            instance.save()

            instance.users.set(User.objects.filter(id__in=form.cleaned_data['users']))
            instance.groups.set(CustomGroup.objects.filter(id__in=form.cleaned_data['groups']))

            instance.inherit = form.cleaned_data.get('inherit', False)
            instance.users_can_view = form.cleaned_data.get('users_can_view', False)
            instance.can_view = form.cleaned_data.get('can_view', False)
            instance.can_add = form.cleaned_data.get('can_add', False)
            instance.can_change = form.cleaned_data.get('can_change', False)
            instance.can_delete = form.cleaned_data.get('can_delete', False)

            instance.save()

            # # Propagate permissions to child nodes if inherit is True
            # if instance.inherit:
            #     child_nodes = List.objects.filter(parent=list_id)
            #     for child in child_nodes:
            #         print(f">>> =================== >>{child} ================== <<<")
            #         child_permission = ListPermission.objects.create(
            #             list_node=child,
            #             inherit=instance.inherit,
            #             can_view=instance.can_view,
            #             can_add=instance.can_add,
            #             can_change=instance.can_change,
            #             can_delete=instance.can_delete,
            #         )
            #         # Propagate users and groups to child node permissions
            #         child_permission.users.set(instance.users.all())
            #         child_permission.groups.set(instance.groups.all())
            # Propagate permissions to child nodes if inherit is True
            if instance.inherit:
                propagate_permissions(instance)

        else:
            print(f"Form errors: {form.errors}")

    else:
        form = ListPermissionForm()

    context = {'form': form, 'list_id': list_id, 'list_permission': list_permission}
    template_url = f"{app_base_ref}/basics/list/settings_template.html"
    
    return render(request, template_url, context)

# def propagate_permissions(instance):
#     # Recursive function to propagate permissions to all descendant levels
#     for child in instance.list_node.get_descendants():
#         child_permission = ListPermission.objects.create(
#             list_node=child,
#             inherit=instance.inherit,
#             can_view=instance.can_view,
#             can_add=instance.can_add,
#             can_change=instance.can_change,
#             can_delete=instance.can_delete,
#         )
#         child_permission.users.set(instance.users.all())
#         child_permission.groups.set(instance.groups.all())

#         if child_permission.inherit:  # Continue propagating
#             propagate_permissions(child_permission)
def propagate_permissions(instance):
    child_nodes = List.objects.filter(parent=instance.list_node.id)
    for child in child_nodes:
        existing_permissions = ListPermission.objects.filter(
            list_node=child,
            inherit=instance.inherit,
            can_view=instance.can_view,
            can_add=instance.can_add,
            can_change=instance.can_change,
            can_delete=instance.can_delete,
            users__in=instance.users.all(),
            groups__in=instance.groups.all(),
        ).distinct()

        if not existing_permissions.exists():
            new_permission = ListPermission.objects.create(
                list_node=child,
                inherit=instance.inherit,
                can_view=instance.can_view,
                can_add=instance.can_add,
                can_change=instance.can_change,
                can_delete=instance.can_delete,
            )
            new_permission.users.set(instance.users.all())
            new_permission.groups.set(instance.groups.all())
            new_permission.save()

            # Call this function recursively only if a new permission is created
            propagate_permissions(new_permission)

# Call this function where needed
# propagate_permissions(instance)


@login_required(login_url='login')
def ajax_get_settings(request):
    if request.method == 'POST':
        list_id = request.POST.get('node_id')
        object = List.objects.get(id=list_id)
        form = ListPermissionForm(instance=object)
        list_permission = ListPermission.objects.filter(active=True, list_node=list_id)
        context = {'form': form, 'list_id': list_id, 'object': object,
                'list_permission': list_permission,}
        template_url = f"{app_base_ref}/basics/list/settings_template.html"
        return render(request, template_url, context )

@login_required(login_url='login')
def ajax_get_node_details_template(request):
    if request.method == 'POST':
        list_id = request.POST.get('node_id')
        object = List.objects.get(id=list_id)

        # get some more details 
        get_last_item = None
        parent = get_object_or_404(List, id=list_id)

        children = parent.get_children()
        ancestors = None
        # iterate through children and get their parents
        if children:
            #print(f" CHILDREN PRESENT {children}")
            children_present = True
        else:
            ancestors = parent.get_ancestors()
        for child in children:
            ancestors = child.get_ancestors()
            if ancestors:
                parent = ancestors[0]
                imm_parent = ancestors.reverse()[0]
            else:
                print(f"{child} has no parent")
        objects = List.objects.filter(id=list_id, active=True).order_by('position')
        objects_count = objects.count()
        if objects_count == 0:
            get_last_item = List.objects.get(id=list_id)

        parent_title = ""
        if object.parent != None:
            parent_title = object.parent.title
        context = {
            'parent': parent_title,
            'title': object.title,
            'description': object.description,
            'created_at': object.created_at,
            'updated_at': object.updated_at,
            # Add other details
            'object': object,
            'last_item': get_last_item,
            'ancestors': ancestors,
            'list_id': list_id,
        }

        # general/specific template
        #===========================================================================
        # Construct the template path dynamically
        template_base = f"{app_base_ref}/jstree_templates"
        template_type_name = f"{object.type}".lower().replace(' ', '_')
        context['template_type_name'] = template_type_name
        specific_template = f"{template_base}/specific/{template_type_name}_template.html"
        template_url = f"{app_base_ref}/basics/list/node_details_template.html"
        template = None
        # Check if the specific template exists
        logger.debug(f">>> === CHECK OS: {specific_template} *** === <<<")
        try:
            loader.get_template(specific_template)
            template = specific_template    
            logger.debug(f">>> === specific_template *** {template} *** === <<<")        
        except TemplateDoesNotExist:
            template = f"{template_base}/general/wbs_general_template.html"
                   
        #============================================================================
        #return JsonResponse(context)
        if template != None:
            template_url = template
            logger.debug(f">>> === SELECTED-TEMPLATE *** {template} *** === <<<")  
        return render(request, template_url, context)


@login_required(login_url='login')
def ajax_update_list_item_description(request):
    if request.method == 'POST':
        object_id = request.POST.get('node_id')
        description = request.POST.get('description')        
        try:            
            object = List.objects.get(id=object_id)
            # Update the fields
            object.description = description
            object.save()
            return JsonResponse({'success': True})
        except List.DoesNotExist:
            pass
    
    return JsonResponse({'success': False})


@login_required(login_url='login')
def ajax_move_node(request):
    #print(f">>> === AJAX MOVE NODE STARTING === <<<")
    try:
        node_id = request.GET.get('node_id')
        target_id = request.GET.get('target_id')
        position = request.GET.get('position')  # 'before', 'after', or 'inside'
        #print(f">>> === GOT POSITION {node_id}=={target_id}==>{position} === <<<")
        node = List.objects.get(id=node_id)
        target = List.objects.get(id=target_id)
        position = 'inside'
        #print(f">>> === AJAX MOVE NODE {node_id} {target_id} {position} {node} {target} === <<<")
        if position == 'before':
            node.move_to(target, 'left')
            #print(f">>> === AJAX MOVE NODE **BEFORE** === <<<")
        elif position == 'after':
            node.move_to(target, 'right')
            #print(f">>> === AJAX MOVE NODE **AFTER** === <<<")
        elif position == 'inside':
            node.move_to(target, 'first-child')
            #print(f">>> === AJAX MOVE NODE **INSIDE** === <<<")
        node.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

# adding new node via context menu
@login_required(login_url='login')
def ajax_add_node(request):
    parent_id = request.GET.get('parent_id')
    title = request.GET.get('title')
    type_id = request.GET.get('type_id')
    type = request.GET.get('type')
    # Initialize other fields from request
    print(f">>> === ADD NODE PARENT ID : {parent_id} TITLE, TYPEID, TYPE {title}, {type_id}, {type} === <<<")
    get_type = None
    title_text = None
    if type_id != None:
        get_type = Type.objects.get(id=type_id)
        title_text = get_type.title
    try:
        parent_node = List.objects.get(id=parent_id, user=request.user, active=True) if parent_id else None
        new_node = List.objects.create(
            user=request.user,
            parent=parent_node,
            title="new_text_view",
            type=get_type,
        )
        
        return JsonResponse({'status': 'success', 'node_id': new_node.id, 'type_title': title_text,})
    except Exception as e:
        print(f"628: Exception encountered: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})


    
@login_required(login_url='login')
def ajax_delete_node(request):    
    if request.method == 'POST':
        object_id = request.POST.get('node_id')
     
        try:            
            List.objects.filter(id=object_id).update(active=False)
            return JsonResponse({'success': True})
        except List.DoesNotExist:
            pass
    
    return JsonResponse({'success': False})


@login_required(login_url='login')
def ajax_copy_node(request):    
    if request.method == 'POST':
        object_id = request.POST.get('node_id')
     
        try:      
            node = List.objects.get(id=object_id)      
            clone_node = List.objects.create(title=node.title, type=node.type, 
                                             parent=node.parent, user=request.user)
            return JsonResponse({'status': 'success', 'node_id': clone_node.id, 'node_text': clone_node.title})
        except List.DoesNotExist:
            pass
    
    return JsonResponse({'status': False})


@login_required(login_url='login')
def ajax_clone_node(request):
    if request.method == 'POST':
        object_id = request.POST.get('node_id')
        node = List.objects.get(id=object_id)
        descendants = node.get_descendants(include_self=True)
        clone_node = List.objects.create(title=node.title + " (cloned) ", parent=node.parent,
                                                type=node.type, 
                                                description=node.description,
                                                user=request.user)
        #print(f">>> STEP1: node {node.id} {node} is cloned as {clone_node.id} {clone_node.id} ")

        # =============== STEP2 =================
        map_nodes = {}
        for descendant in node.get_descendants().filter(active=True):
            step2_flag = True
            #print(f">>> STEP2: Map nodes {descendant.parent.id}|{descendant.id}")
            if descendant.parent.id in map_nodes:
                map_nodes[descendant.parent.id].update({descendant.id: descendant.title})
            else:
                map_nodes[descendant.parent.id] = {descendant.id: descendant.title}

        # =============== STEP3 =================
        backup_nodes = map_nodes
        #print(f">>> STEP3: Cloned Node takes place {map_nodes} and backup nodes {backup_nodes}")
        map_nodes[clone_node.id] = map_nodes[node.id]
        del map_nodes[node.id]
        #print(f">>> STEP4: Move to cloned node {map_nodes}")
        if clone_node.id in map_nodes:
            for k,v in map_nodes[clone_node.id].items():
                test2 = List.objects.get(id=k)
                ic = List.objects.create(title=v, parent_id=clone_node.id, 
                                                type=test2.type,
                                                description=test2.description,
                                                user=request.user)
                # recurse from here
                # recurse_clone_from_map(k, ic.id, map_nodes)
                recurse_clone_from_map(k, ic, map_nodes, List, request)
                #print(f"IMMEDIATE CLONE {node.id}, {node}: {ic.parent.id}, {ic.parent}, {ic.id}")
            del map_nodes[clone_node.id]
        #print(f"CLONE_NODE {clone_node.id} from NODE {node.id}")
        #print(f"MAP NODES after cloning: {map_nodes}")
        return JsonResponse({'status': 'success', 'node_id': clone_node.id, 'node_text': clone_node.title})



@login_required(login_url='login')
def list_js_tree(request):
    objects = List.objects.filter(parent=None, active=True, deleted=False).order_by('position', '-created_at')
    objects_count = objects.count()

    permitted_nodes = get_permitted_nodes_for_user(request, objects)
    objects = permitted_nodes
    objects_count = permitted_nodes.count()

    context = {'page': 'list_js_tree', 'objects': objects, 'objects_count': objects_count}
    template_url = f"{app_base_ref}/basics/list/list_js_tree.html"
    print(f">>> === (((((((((((((((((((((((((()))))))))))))))))))))))))) === <<<")
    return render(request, template_url, context)

@login_required(login_url='login')
def list_js_tree_id(request, list_id):
    object = List.objects.get(id=list_id)
    objects = List.objects.filter(id=list_id, active=True).order_by('position', '-created_at')
    objects_count = objects.count()
    
    # get the organization from the list id
    print(f">>> === LIST ID {list_id} {object} type: {object.type} === <<<")
    root_object = None
    mapping_wbs = MappingWBS.objects.filter(list_id=object.id).first()
    organization=None
    organization_id=None
    if mapping_wbs == None:
        root_object = object.get_root()
        print(f">>> === ROOT ||| {root_object} type: {object.type}=== <<<")
        list = List.objects.get(id=root_object.id)
        mapping_wbs = MappingWBS.objects.get(list=list)
        organization = mapping_wbs.organization.name
        organization_id = mapping_wbs.organization.id
    else:
        organization = mapping_wbs.organization.name
        organization_id = mapping_wbs.organization.id
    permitted_nodes = get_permitted_nodes_for_user(request, objects)
    objects = permitted_nodes
    objects_count = permitted_nodes.count()
    
    logger.debug(f">>> === PN {objects} PNC {objects_count} === <<<")
    context = {'page': 'list_js_tree', 'list_id': list_id, 'object': object, 
               'objects': objects, 'objects_count': objects_count, 
               'mapping_wbs': mapping_wbs, 'organization_id': organization_id,
               'organization': organization,
               'root_object': root_object,}
    template_url = f"{app_base_ref}/basics/list/list_js_tree_id.html"
    return render(request, template_url, context)
# end experiment jstree
######################################################################################
@login_required(login_url='login')
def ajax_update_tree_field(request):
    model_name = request.POST.get('model')
    wbs_model_name = request.POST.get('wbs')
    field_name = request.POST.get('field')
    value = request.POST.get('value')
    idx = request.POST.get('id')
    object_id = request.POST.get('object_id')
    print(f">>> === AJAX UPDATE DTC FIELD {model_name} === <<<")
    Model = apps.get_model('app_baseline', model_name)  # Update 'your_app_name'
    obj = None
    obj = Model.objects.get(id=idx)
    setattr(obj, field_name, value)
    obj.save()
    
    if wbs_model_name in my_wbs:
        print(f">>> === |||| CHECKING WBS MODEL NAME {wbs_model_name} |||| === <<<")
        wbs_model = wbs_model_name.replace(" ", "")
        Model = apps.get_model('app_web', wbs_model)  # Update 'your_app_name'
        print(f">>> === AJAX check -- {Model} === <<<")
        obj = None
        obj = Model.objects.get(id=idx)
        if field_name == 'title':
            field_name = 'name'
        setattr(obj, field_name, value)
        print(f">>> === AJAX UPDATE DTC FIELD AW field_name, value: {field_name}, {value} === <<<")
        obj.save()

    return JsonResponse({'success': True})