# all imports
from ..all_view_imports import *

# config
from ..._common.config.config import *

# specific imports
from ...forms.user.form_user import *
from ...forms.list.form_list import *
from ...forms.type.form_type import *

from ...models.user.model_user import *
from ...models.list.model_list import *
from ...models.type.model_type import *
from ...decorators.authz.decorator_authorization import *

# which app is being referred
app_base_ref = base_app_ref

@login_required(login_url='login')
def type_home(request):
    objects = Type.objects.filter(user=request.user, parent=None, active=True, deleted=False).order_by('position', '-created_at')
    objects_count = objects.count()
    context = {'page': 'type_home', }
    form = TypeForm(request)
    if request.method == 'POST':
        objects = Type.objects.filter(user=request.user, parent=None, active=True, deleted=False).order_by('position', '-created_at')
        objects_count = objects.count()
        form = TypeForm(request.user, data=request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.parent = None
            form.save()
            context['objects'] = objects
        else:
             context['error'] = "Form is Invalid"
             print(f">>> === FORM INVALID ERROR {form} === <<<")
        
    context = {'page': 'type_home', 'objects': objects, 'objects_count': objects_count, 
               'form': form, 'active_tab': 'type_home',}
    template_url = f"{app_base_ref}/basics/type/type_home.html"
    return render(request, template_url, context)

@login_required(login_url='login')
def delete_type_item(request, type_id):    
    context = {'page': 'type_home', }
    object = Type.objects.filter(id=type_id).update(active=False)
    parent=get_object_or_404(Type, id=type_id).parent
    template_url = f"{app_base_ref}/basics/type/type_home.html"       
    objects = Type.objects.filter(user=request.user, active=True, deleted=False).order_by('-created_at','position')
    context = {'page': 'type_home', 'objects': objects}
    if request.GET.get('type_home') != None and request.GET.get('type_home') == 'yes':
        return redirect("type_items", list_id=parent.id)
    return redirect("type_home")

# 
#  List children
#
@login_required(login_url='login')
def type_items(request, type_id):   
    context = {'page': 'type_home', }
    parent = get_object_or_404(Type, pk=type_id,user=request.user,)
    #print(f">>> === PARENT node is {parent} === <<<")   
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
                print(f"{child} has no parent")
    objects = Type.objects.filter(parent_id=type_id, user=request.user,active=True).order_by('position')
    objects_count = objects.count()
    if objects_count == 0:
        get_last_item = Type.objects.get(id=type_id)
    # post method processing
    list = TypeForm(request.user, current_parent_id=type_id)
    if request.method == 'POST':
        list = TypeForm(request.user, current_parent_id=type_id, data=request.POST)
        if list.is_valid():
            parent = list.cleaned_data['parent']
            list = list.save(commit=False)
            list.parent = parent
            list.user = request.user
            list.save()
            #print(f">>> === Type Item {list} === <<<")
        list = TypeForm(request.user, current_parent_id=type_id, )
        objects = Type.objects.filter(parent_id=type_id, user=request.user,active=True).order_by('position')
        objects_count = objects.count()

    # sending the details to template
    context = {'page': 'type_home', 'objects': objects, 'objects_count': objects_count,
               'parent_id': type_id, 'last_item': get_last_item,
               'ancestors':ancestors,}
    template_url = f"{app_base_ref}/basics/type/type_items.html"
    return render(request, template_url, context)
#######################################################################################
# copy and deep-copy / clone

@login_required(login_url='login')
def clone_type_items(request, type_id):
    node = Type.objects.get(id=type_id)
    clone_node = Type.objects.create(title=node.title, parent=node.parent, user=request.user)
    #print(f"CLONE node: {clone_node}")
    url = None
    if request.GET.get('type') != None and request.GET.get('type') == "yes":
        url = reverse('type_home')
    else:
        url = reverse('type_items', args=[node.parent.id])
    return redirect(url)

@login_required(login_url='login')
def deep_clone_type_items(request, type_id):
    node = Type.objects.get(id=type_id)
    descendants = node.get_descendants(include_self=True)
    clone_node = Type.objects.create(title=node.title + " (cloned) ", parent=node.parent, 
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
            test2 = Type.objects.get(id=k)
            ic = Type.objects.create(title=v, parent_id=clone_node.id, 
                                            description=test2.description,
                                            user=request.user)
            # recurse from here
            # recurse_clone_from_map(k, ic.id, map_nodes)
            recurse_clone_from_map(k, ic, map_nodes, Type, request)
            #print(f"IMMEDIATE CLONE {node.id}, {node}: {ic.parent.id}, {ic.parent}, {ic.id}")
        del map_nodes[clone_node.id]
    #print(f"CLONE_NODE {clone_node.id} from NODE {node.id}")
    #print(f"MAP NODES after cloning: {map_nodes}")
    url = None
    if request.GET.get('type') != None and request.GET.get('type') == "yes":
        url = reverse('type_home')
    else:
        url = reverse('type_items', args=[node.parent.id])
    return redirect(url)

def recurse_clone_from_map(k, ic, map_nodes, mainobject, request):
    if k in map_nodes:
        #print(f" RECURSE ******* {k}")
        for k1,v1 in map_nodes[k].items():
            test3 = Type.objects.get(id=k1)
            iic = mainobject.objects.create(title=v1, parent_id=ic.id, 
                                            description=test3.description,
                                            user=request.user)
            if k1 in map_nodes:
                #print(f" ******* >>>>> TEST {k1}")
                recurse_clone_from_map(k1, iic, map_nodes, mainobject, request)
    return map




#######################################################################################
#
# AJAX related: List top level
#
@login_required(login_url='login')
def ajax_update_type_item(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')
        title = request.POST.get('title')
        done = request.POST.get('done')   
        save_field_done = False
        if done == "true":
            save_field_done=True
        #print(f">>> === AJAX UPDATE LIST ITEM {title} === <<<")
        
        try:            
            object = Type.objects.get(id=object_id)
            # Update the fields
            object.title = title
            object.done = save_field_done
            object.save()
            print(f">>> === (saved) AJAX UPDATE TYPE ITEM {title} === <<<")
            # end of card movement update
            return JsonResponse({'success': True})
        except Type.DoesNotExist:
            pass
    
    return JsonResponse({'success': False})

@login_required(login_url='login')
def ajax_rename_type_item(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')
        title = request.POST.get('title')
        print(f">>> === AJAX RENAME TYPE ITEM {title} {object_id} === <<<")
        
        try:            
            object = Type.objects.get(id=object_id)
            # Update the fields
            object.title = title
            object.save()
            print(f">>> === (saved) AJAX RENAME TYPE ITEM {title} === <<<")
            # end of card movement update
            return JsonResponse({'success': True})
        except Type.DoesNotExist:
            pass
    
    return JsonResponse({'success': False})

@login_required(login_url='login')
def ajax_update_type_sorted(request):
    if request.method == 'POST':
        ajax_data = request.POST['sorted_list_data']
        new_data = ajax_data.replace("[",'')
        new_data = new_data.replace("]",'')
        sorted_list = new_data.split(",")
        seq = 1
        #print(f">>> === AJAX UPDATE SORTED === <<<")
        for item in sorted_list:
            str = item.replace('"','')
            position = str.split('_')
            #print(f">>> === AJAX UPDATE SORTED {position} === <<<")
            Type.objects.filter(pk=position[0]).update(position=seq)
            seq = seq + 1
        context = {'page': 'Sorted Value', 
                   'active_tab': 'sorted_value',
                   'ajax_data': ajax_data}
        return JsonResponse({'success': True})
    
######################################################################################
# experiment jstree

@login_required(login_url='login')
def ajax_type_get_tree_data(request):
    root_nodes = Type.objects.filter(user=request.user, parent=None, active=True, deleted=False).order_by('position', '-created_at')
    data = []

    def add_node_and_children(node):
        level = node.level  # Assuming nodes have a level attribute
        is_opened = level < 2  # Open up to level 2 (0-indexed)
        if level < 2:
            is_opened = "true"
        #print(f">>> === **** LEVEL {level}:{is_opened} **** === <<<")
        parent = node.parent.id if node.parent else '#'
        data.append({'id': str(node.id), 'parent': str(parent), "type": "folder", 'text': node.title, 'state': {'opened': is_opened} })

        for child in node.get_children():
            if child.active == True:
                add_node_and_children(child)
                # edge case node char length to be specific to avoid overlap on div

    for root in root_nodes:
        add_node_and_children(root)
    return JsonResponse(data, safe=False)


@login_required(login_url='login')
def ajax_type_get_tree_data_id(request):
    if request.method == 'POST':
        type_id = request.POST.get('type_id')
        root_nodes = Type.objects.filter(user=request.user, id=type_id, active=True, deleted=False).order_by('position', '-created_at')
        data = []

        def add_node_and_children(node):
            level = node.level  # Assuming nodes have a level attribute
            is_opened = level < 2  # Open up to level 2 (0-indexed)
            if level < 2:
                is_opened = "true"
            #print(f">>> === **** LEVEL {level}:{is_opened} **** === <<<")
            parent = node.parent.id if node.parent else '#'
            data.append({'id': str(node.id), 'parent': str(parent), "type": "folder", 'text': node.title, 'state': {'opened': is_opened} })

            for child in node.get_children():
                if child.active == True:
                    add_node_and_children(child)
                    # edge case node char length to be specific to avoid overlap on div

        for root in root_nodes:
            add_node_and_children(root)
        response_data = {
            'data': data,
        }
        return JsonResponse(response_data, safe=False)


@login_required(login_url='login')
def ajax_type_get_node_details(request, type_id):
    object = Type.objects.get(id=type_id)
    print(f">>> === {type_id}::{object.parent} === <<<")
    parent_title = ""
    if object.parent != None:
        parent_title = object.parent.title
    details = {
        'parent': parent_title,
        'title': object.title,
        'description': object.description,
        'created_at': object.created_at,
        'updated_at': object.updated_at,
        # Add other details
    }
    return JsonResponse(details)

@login_required(login_url='login')
def ajax_update_type_item_description(request):
    if request.method == 'POST':
        object_id = request.POST.get('node_id')
        description = request.POST.get('description')        
        try:            
            object = Type.objects.get(id=object_id)
            # Update the fields
            object.description = description
            object.save()
            return JsonResponse({'success': True})
        except Type.DoesNotExist:
            pass
    
    return JsonResponse({'success': False})


@login_required(login_url='login')
def ajax_type_move_node(request):
    print(f">>> === AJAX MOVE NODE STARTING === <<<")
    try:
        node_id = request.GET.get('node_id')
        target_id = request.GET.get('target_id')
        position = request.GET.get('position')  # 'before', 'after', or 'inside'
        print(f">>> === GOT POSITION {node_id}=={target_id}==>{position} === <<<")
        node = Type.objects.get(id=node_id)
        target = Type.objects.get(id=target_id)
        position = 'inside'
        print(f">>> === AJAX MOVE NODE {node_id} {target_id} {position} {node} {target} === <<<")
        if position == 'before':
            node.move_to(target, 'left')
            print(f">>> === AJAX MOVE NODE **BEFORE** === <<<")
        elif position == 'after':
            node.move_to(target, 'right')
            print(f">>> === AJAX MOVE NODE **AFTER** === <<<")
        elif position == 'inside':
            node.move_to(target, 'first-child')
            print(f">>> === AJAX MOVE NODE **INSIDE** === <<<")
        node.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

# adding new node via context menu
@login_required(login_url='login')
def ajax_type_add_node(request):
    parent_id = request.GET.get('parent_id')
    title = request.GET.get('title')
    # Initialize other fields from request
    #print(f">>> === ADD NODE PARENT ID : {parent_id} === <<<")
    try:
        parent_node = Type.objects.get(id=parent_id, user=request.user, active=True) if parent_id else None
        new_node = Type.objects.create(
            user=request.user,
            parent=parent_node,
            title="new_text_view",
        )
        #print(f">>> === *** CREATE NODE {new_node.id} on parent {parent_node}**** === <<<")
        return JsonResponse({'status': 'success', 'node_id': new_node.id})
    except Exception as e:
        print(f"Exception encountered: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required(login_url='login')
def ajax_type_delete_node(request):    
    if request.method == 'POST':
        object_id = request.POST.get('node_id')
     
        try:            
            Type.objects.filter(id=object_id).update(active=False)
            return JsonResponse({'success': True})
        except Type.DoesNotExist:
            pass
    
    return JsonResponse({'success': False})

@login_required(login_url='login')
def ajax_type_copy_node(request):    
    if request.method == 'POST':
        object_id = request.POST.get('node_id')
     
        try:      
            node = Type.objects.get(id=object_id)      
            clone_node = Type.objects.create(title=node.title, parent=node.parent, user=request.user)
            return JsonResponse({'status': 'success', 'node_id': clone_node.id, 'node_text': clone_node.title})
        except Type.DoesNotExist:
            pass
    
    return JsonResponse({'status': False})


@login_required(login_url='login')
def ajax_type_clone_node(request):
    if request.method == 'POST':
        object_id = request.POST.get('node_id')
        node = Type.objects.get(id=object_id)
        descendants = node.get_descendants(include_self=True)
        clone_node = Type.objects.create(title=node.title + " (cloned) ", parent=node.parent, 
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
                test2 = Type.objects.get(id=k)
                ic = Type.objects.create(title=v, parent_id=clone_node.id, 
                                                description=test2.description,
                                                user=request.user)
                # recurse from here
                # recurse_clone_from_map(k, ic.id, map_nodes)
                recurse_clone_from_map(k, ic, map_nodes, Type, request)
                #print(f"IMMEDIATE CLONE {node.id}, {node}: {ic.parent.id}, {ic.parent}, {ic.id}")
            del map_nodes[clone_node.id]
        #print(f"CLONE_NODE {clone_node.id} from NODE {node.id}")
        #print(f"MAP NODES after cloning: {map_nodes}")
        return JsonResponse({'status': 'success', 'node_id': clone_node.id, 'node_text': clone_node.title})



@login_required(login_url='login')
def type_js_tree(request):
    objects = Type.objects.filter(user=request.user, parent=None, active=True, deleted=False).order_by('position', '-created_at')
    objects_count = objects.count()
    context = {'page': 'type_js_tree', 'objects': objects, 'objects_count': objects_count}
    template_url = f"{app_base_ref}/basics/type/type_js_tree.html"
    return render(request, template_url, context)

@login_required(login_url='login')
def type_js_tree_id(request, type_id):
    object = Type.objects.get(id=type_id)
    objects = Type.objects.filter(user=request.user, id=type_id, active=True, deleted=False).order_by('position', '-created_at')
    objects_count = objects.count()
    context = {'page': 'type_js_tree', 'type_id': type_id, 'object': object, 'objects': objects, 'objects_count': objects_count}
    template_url = f"{app_base_ref}/basics/type/type_js_tree_id.html"
    return render(request, template_url, context)
# end experiment jstree
######################################################################################