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
from django.db.models import Q, Count
from ..forms import *
from ..decorators import *
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
@user_in_group(['View_Value_Group'])
@check_value_permissions_type('edit')
def boards_home(request, value_type, pk):
    model_name = value_type
    model_class = get_model_class(value_type)
    obj = model_class.objects.get(id=pk)
    lc_model_name = model_name.lower()
    board_lookup = {lc_model_name: obj}
    # here we list all projects
    newtodolist = Board.objects.filter(**board_lookup, active=True, deleted=False).order_by('position')
    print(f">>>>>>>>>>>>>>>>>> BOARDS {newtodolist} {board_lookup}")
    newtodolist_count = newtodolist.count()
    form = BoardForm(request.user)
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
                'pagination_on': pagination_on,
                 'value_type': value_type, 'object':obj,
                 'page': 'Boards Home', 'active_tab': 'boards_home', 'boards': newtodolist}

    return render(request, "app_xpresskanban/boards/boards_home.html", context)

## ADD NEW BOARD
@login_required(login_url='login')
@user_in_group(['View_Value_Group'])
@check_value_permissions_type('edit')
def create_board(request, value_type, pk):
    form = BoardForm()
    model_class = get_model_class(value_type)
    obj = model_class.objects.get(id=pk)
    board_lookup = {value_type.lower(): obj}
    boards = Board.objects.filter(**board_lookup)
    if request.method == 'POST':
        form = BoardForm(request.POST)
        print(f">>>>>>>>>>>>>>> BOARD form POST1")
        if form.is_valid():
            print(f">>>>>>>>>>>>>>> BOARD form POST2 VALID")
            setattr(form.instance, value_type.lower(), obj)
            form.instance.author = request.user
            board = form.save()    
            print(f">>> === BOARD created {board} {board.id} === <<<")
            # Board group is created for granting access to the group
            board_view_group = f"Board_{board.id}_{value_type}_{pk}_view"
            board_edit_group = f"Board_{board.id}_{value_type}_{pk}_edit"
            board_admin_group = f"Board_{board.id}_{value_type}_{pk}_admin"
            view_board_users = CustomGroup.objects.create(name=board_view_group,active=True,author=request.user,)
            edit_board_users = CustomGroup.objects.create(name=board_edit_group,active=True,author=request.user,)
            admin_board_users = CustomGroup.objects.create(name=board_admin_group,active=True,author=request.user,)
            owner_of_group = User.objects.filter(username=request.user).first()
            owner_of_group.groups.add(admin_board_users)
            # End Board group is created for granting access to the group
            url_ref = reverse('boards_home', args=[value_type, pk])          
            return redirect(url_ref)
    else:
        form = BoardForm()
    
    context = {'page': 'Add ' + value_type, 
               'form': form, 
               'value_type': value_type, 'pk':pk}
    template_name = 'app_xpresskanban/boards/create_board.html'
    return render(request, template_name, context)
# board ==> ops_value
@login_required(login_url='login')
def ops_board(request, value_type, board_id):
    print(f">>>>>>>>>>.. RECEIVED FOR OPS BOARD ")
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
                    print(f">>>>>>>>>>>> BULK DELETE {id}")
                    Board.objects.filter(id=board_id).update(active=False, deleted=False,  
                                                       author=request.user)
            elif bulk_ops == "bulk_done":
                for id in selected_project_ids:
                    Board.objects.filter(id=board_id).update(done=True,  author=request.user)
                    check_board = Board.objects.get(id=board_id)
                    print(f">>>>> checking the bulk_done {check_board.done}")
            print(f">>>>>>>>>>>.FORM. {bulk_ops} is bulk_ops, pagination {pagination}")
            context = {'bulk_ops': bulk_ops, 'pagination': pagination, 
                       'selected_project_ids':selected_project_ids,
                       'value_type': value_type, 'page': 'Board'}
            return render(request, 'app_xpresskanban/boards/bulk_board_ops.html', context)

@login_required(login_url='login')
def sorted_boards(request, value_type, pk):   
    model_class = get_model_class(value_type)
    obj = model_class.objects.get(id=pk)
    if request.method == 'POST':
        ajax_data = request.POST['sorted_list_data']
        new_data = ajax_data.replace("[",'')
        new_data = new_data.replace("]",'')
        sorted_list = new_data.split(",")
        seq = 1
        for item in sorted_list:
            str = item.replace('"','')
            position = str.split('_')
            Board.objects.filter(pk=position[0]).update(position=seq)
            seq = seq + 1
        context = {'page': 'Sorted Value', 
                   'active_tab': 'sorted_value',
                   'value_type': value_type,
                   'pk': pk,
                   'object': obj,
                   'ajax_data': ajax_data}
        return render(request, 'app_xpresskanban/boards/boards_home.html',context)
    
@login_required(login_url='login')
@check_board_permissions_type('edit')
def delete_item(request, value_type, pk, board_id):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    url_ref = reverse('boards_home', args=[model_name, pk])
    item_class = Board
    item = get_object_or_404(item_class,id=board_id)
    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        context = {'value_type': value_type, model_name: obj, 'object': obj, 'item': item}
        if request.method == 'POST':
            item_class.objects.filter(id=board_id).update(active=False, author=request.user)     
            return redirect(url_ref)
        return render(request, 'app_xpresskanban/boards/delete_item_confirm.html', context)
    else:
        # Handle invalid model name
        return redirect('kanban_home')  # Redirect to a proper error page or other handling
@login_required(login_url='login')
@check_board_permissions_type('view')
def view_item(request, value_type, pk, board_id):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    item_class = Board
    
    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        item = get_object_or_404(item_class,id=board_id)
        context = {'value_type': value_type, model_name: obj, 'object': obj, 'item': item}
        return render(request, 'app_xpresskanban/boards/view_item.html', context)
    else:
        # Handle invalid model name
        return redirect('kanban_home')  # Redirect to a proper error page or other handling

@login_required(login_url='login')
@check_board_permissions_type('edit')
def edit_item(request, value_type, pk, board_id):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    item_class = Board
    url_ref = reverse('boards_home', args=[model_name, pk])
    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        item = get_object_or_404(item_class,id=board_id)
        form = BoardForm(instance=item)
        print(f">>>>>>>>>>>>> EDIT ITEM {item}")
        if request.method == 'POST':
            form = BoardForm(request.POST, instance=item)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect(url_ref)
            else:
                print(f">>>>> FORM IS INVALID: {form}")
        else:
            form = BoardForm(instance=item)
        context = {'page': 'Edit ' + model_name,'form': form, model_name: obj
                   ,'value_type': value_type, 'object': obj, 'item': item}
        return render(request, 
                      'app_xpresskanban/boards/edit_item.html', context)
    else:
        # Handle invalid model name
        return redirect('kanban_home')  # Redirect to a proper error page or other handling
    
@login_required(login_url='login')
@check_board_permissions_type('view')
def list_deleted_items(request, value_type, pk):
    model_name = value_type
    model_class = None
    item_count = 0
    model_class = get_model_class(model_name)
    obj = get_object_or_404(model_class, pk=pk)
    if model_class is not None:
        context = {'page': 'Restore Deleted Boards'}
        # here we list all projects deleted and restore
        item_class = Board
        newtodolist = item_class.objects.filter(active=False, deleted=False).order_by('position')
        newtodolist_count = newtodolist.count()
        form = BoardForm(request.user)
        url_ref = reverse('boards_home', args=[model_name, pk])
        if request.method == 'POST':
            form = BoardForm(request.user, request.POST)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                item_count = newtodolist.count()
                return redirect(url_ref)
            else:
                print(f"form is invalid {form}")
        context = {'newtodolist': newtodolist,'form':form, 
                   'newtodolist_count': newtodolist_count, 'value_type': value_type,
                   'pk': pk, 'item_count': item_count,
                   'object': obj}
        return render(request, 'app_xpresskanban/boards/list_deleted_items.html', context)
    
### bulk operations ###
@login_required(login_url='login')
@check_board_permissions_type('edit')
def bulk_restore_deleted_items(request, value_type, pk):
    model_name = value_type
    model_class = None
    item_class = Board
    model_class = get_model_class(model_name)
    obj = get_object_or_404(model_class, pk=pk)

    if model_class is not None:
        if request.method == 'POST':
            form_data = request.POST
            selected_project_ids = request.POST.getlist('restore_project_box')        
            bulk_ops = form_data.get('bulk_project_ops')
            if bulk_ops == "bulk_restore":
                for id in selected_project_ids:
                    item_class.objects.filter(id=id).update(active=True,  author=request.user)
            elif bulk_ops == "bulk_not_done":
                for id in selected_project_ids:
                    item_class.objects.filter(id=id).update(done=False,  author=request.user)
            elif bulk_ops == "bulk_delete_permanently":
                for id in selected_project_ids:
                    item_class.objects.filter(id=id).update(active=False, deleted=True,  author=request.user)
            pagination = form_data.get('pagination')
            print(f">>>>>>>>>>>.FORM. {bulk_ops} is bulk_ops, pagination {pagination}")
            context = {'bulk_ops': bulk_ops, 'pagination': pagination, 
                    'selected_project_ids':selected_project_ids, 'value_type': value_type,
                   'pk': pk,
                   'object': obj}
        return render(request, 'app_xpresskanban/bulk_restore_ops_value.html', context)
    
# restore: listing the values that needs to be restored
@login_required(login_url='login')
@check_board_permissions_type('edit')
def restore_an_item(request, value_type, pk, board_id):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    item_class = Board
    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        item = get_object_or_404(item_class, id=board_id)
        context = {'object': obj, 'value_type': value_type,
                   'pk': pk, 'item': item}
        url_ref = reverse('boards_home', args=[model_name, pk])
        if request.method == 'POST':
            item_class.objects.filter(id=board_id).update(active=True,  author=request.user)
            return redirect(url_ref)
        return render(request, 'app_xpresskanban/boards/restore_an_item.html', context)
# kanban board
@login_required(login_url='login')
@check_board_permissions_type('view')
def kanban_board(request, value_type, pk, board_id):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    #
    #
    matching_groups = getattr(request, 'matching_groups', [])
    for group_name in matching_groups:
        print(f">>> ==== ********** The user is in group: {group_name} === <<<")
    #
    item_class = Board
    column_class = BoardColumns
    obj = get_object_or_404(model_class, pk=pk)
    item = get_object_or_404(item_class, id=board_id)

    board_columns = None
    board_columns_first = None
    try:
        board_columns = column_class.objects.filter(board=item, active=True, deleted=False).order_by('position')
        board_columns_first = column_class.objects.filter(board=item, active=True, deleted=False).first()
        #print(f">>>>>>>>>>>>>>>>>>>>> BOARD COLUMNS FIRST {board_columns_first}")
    except column_class.DoesNotExist:
        board_columns = None
        #print(f">>>> BoardColumns is null for {item}")
    lc_model_class = model_name.lower()
    lc_item_class = "board"
    column_class = "BoardColumns"
    val_lookup = {lc_model_class: obj}
    item_lookup = {lc_item_class: item}
    context = {}
    newtodolist = CORE_HSDB.objects.filter(active=True, **val_lookup, 
                            **item_lookup , parent=None).order_by('position', 'swimlane')
    newtodolist_count = newtodolist.count()
    form = CORE_HSDB_Form(request.user)
    url_ref = reverse('kanban_board', args=[model_name, pk, board_id])

    # experiment 1 card count
    board_columns_details = BoardColumns.objects.filter(board=item, active=True, deleted=False)
    #print(f">>>>>>>>>>>>> BOARD COLUMNS {board_columns_details}")
    card_count_details = {}
    for column in board_columns_details:
        col_obj = BoardColumns.objects.get(id=column.id)
        #card_count_details[column.id] = CORE_HSDB.objects.filter(**val_lookup, **item_lookup, column=col_obj).count()
        card_count_details[column.id] = CORE_HSDB.objects.filter(
                **val_lookup,
                **item_lookup,
                column=col_obj, active=True,
            ).exclude(swimlane__title__iexact='Expedite').count()
    #print(f">>> === ************************* CARD COUNT DETAILS {card_count_details} === <<<")
    column_policy_details = {}
    for column in board_columns_details:
        col_obj = BoardColumns.objects.get(id=column.id)
        if col_obj.policies != "":
            column_policy_details[column.id] = convert_to_ul_li(col_obj.policies)
    print(f">>>>>>>>>>>>>>> {column_policy_details}")
    get_return_info = card_metrics_update(value_type, pk, board_id)
    average_cycle_time = get_return_info['average_cycle_time']
    average_lead_time = get_return_info['average_lead_time']  
    average_wip = get_return_info['average_wip']

    dates = get_return_info['dates'] 
    columns = get_return_info['columns'] 
    card_counts_by_date = get_return_info['card_counts_by_date'] 

    cfd_display = get_return_info['cfd_display']
    throughput_last_14_days = get_return_info['throughput_last_14_days']  
    newtodolist = get_return_info['newtodolist']  

    # board_history
    board_history = BoardHistory.objects.filter(board=item).last()
    #print(f">>>>>>>>>>>>>>>> ========= board_history {board_history}")
    if model_class is not None:
        if request.method == 'POST':
            newtodolist = None
            newtodolist_count = 0
            action = request.POST.get('action')
            if action == "Search/Clear":
                query = request.POST.get('title')
                if query:
                    newtodolist = CORE_HSDB.objects.filter(
                            Q(title__icontains=query) |
                            Q(description__icontains=query)).filter(**item_lookup)
                    newtodolist_count = newtodolist.count()
                else:
                    newtodolist = CORE_HSDB.objects.filter(active=True, **val_lookup, 
                                            **item_lookup , parent=None).order_by('position', 'swimlane')
                    newtodolist_count = newtodolist.count()
                if query is None:
                    query = ''
            else:
                form = CORE_HSDB_Form(request.user, current_parent_id=None, data=request.POST)
                if form.is_valid():
                    workitemtype = form.cleaned_data['workitemtype']           
                    setattr(form.instance, value_type.lower(), obj)
                    form.instance.author = request.user
                    setattr(form.instance, lc_item_class, item)
                    setattr(form.instance, "column", board_columns_first)                    
                    card = form.save()
                    ## first column 
                    CardMovement.objects.create(card=card,
                                    source_column=board_columns_first, target_column=board_columns_first, 
                                    author=request.user)

                    newtodolist = CORE_HSDB.objects.filter(active=True, **val_lookup, 
                                           **item_lookup , parent=None).order_by('swimlane', 'position')
                    newtodolist_count = newtodolist.count()
                    return redirect(url_ref)
                else:
                    print(f"form is invalid {form}")
        global_counter = 1
        only_none_swimlane=True
        swimlane_titles = Swimlane.objects.filter(board=item, active=True).values('title').annotate(title_count=Count('title'))
        if swimlane_titles.filter(title_count__gt=0).exists():
            only_none_swimlane=False
        grouped_cards = group_cards(newtodolist, item)
        board_cards = CORE_HSDB.objects.filter(board=item,active=True).order_by('position')
        #
        #
        # CFD data testing
        #
        #
        # cfdData = [
        # { 'date': '2023-01-01', 'Backlog': 10, 'Todo': 5, 'WIP': 3, 'Blocked': 1, 'Done': 1 },
        # { 'date': '2023-01-02', 'Backlog': 18, 'Todo': 6, 'WIP': 3, 'Blocked': 2, 'Done': 2 },
        # { 'date': '2023-01-03', 'Backlog': 12, 'Todo': 7, 'WIP': 3, 'Blocked': 2, 'Done': 3 },
        # { 'date': '2023-01-04', 'Backlog': 16, 'Todo': 6, 'WIP': 4, 'Blocked': 2, 'Done': 4 },
        # { 'date': '2023-01-05', 'Backlog': 15, 'Todo': 5, 'WIP': 5, 'Blocked': 2, 'Done': 5 },
        # { 'date': '2023-01-06', 'Backlog': 4, 'Todo': 4, 'WIP': 6, 'Blocked': 2, 'Done': 6 },
        # { 'date': '2023-01-07', 'Backlog': 4, 'Todo': 3, 'WIP': 7, 'Blocked': 3, 'Done': 7 },
        # { 'date': '2023-01-08', 'Backlog': 3, 'Todo': 2, 'WIP': 7, 'Blocked': 4, 'Done': 8 },
        # { 'date': '2023-01-09', 'Backlog': 2, 'Todo': 1, 'WIP': 7, 'Blocked': 4, 'Done': 9 },
        # { 'date': '2023-01-10', 'Backlog': 1, 'Todo': 0, 'WIP': 6, 'Blocked': 5, 'Done': 10 },
        # { 'date': '2023-01-11', 'Backlog': 0, 'Todo': 0, 'WIP': 5, 'Blocked': 5, 'Done': 11 },
        # { 'date': '2023-01-12', 'Backlog': 0, 'Todo': 0, 'WIP': 5, 'Blocked': 6, 'Done': 12 },
        # { 'date': '2023-01-13', 'Backlog': 0, 'Todo': 0, 'WIP': 5, 'Blocked': 6, 'Done': 13 },
        # { 'date': '2023-01-14', 'Backlog': 0, 'Todo': 0, 'WIP': 5, 'Blocked': 7, 'Done': 14 },
        # ]
        cfdData = get_return_info['cfdData']
        print(f">>> === POLICY DETAILS: {column_policy_details} === <<<")
        context = {
                'newtodolist': newtodolist,'form':form, 
                'newtodolist_count': newtodolist_count,
                'object': obj, 'value_type': value_type,
                'pk': pk, 'item': item, 'board_columns': board_columns,
                'global_counter': global_counter,
                'card_count_details':card_count_details, 'board_columns_details': board_columns_details,
                'column_policy_details':column_policy_details,
                'board_history': board_history,
                'average_lead_time': average_lead_time,
                'average_cycle_time': average_cycle_time,
                'throughput_last_14_days':throughput_last_14_days,
                'average_wip':average_wip,
                'cfd_display': cfd_display,
                'grouped_cards':grouped_cards, 'board_cards': board_cards,
                'columns': columns, 'dates': dates, 'card_counts_by_date':card_counts_by_date,
                'only_none_swimlane':only_none_swimlane,
                'cfdData': cfdData}
        return render(request, 'app_xpresskanban/boards/kanban_board.html', context)
#
#
# group the cards 
#
#
def group_cards(cards, item):
    swimlanes = Swimlane.objects.filter(active=True, board=item).order_by('position')
    grouped_cards = {}
    none_swimlane = None
    for swimlane in swimlanes:
        print(f">>> ==== SWIMLANE: {swimlane} board:{item} === <<<")
        cards = swimlane.swimlane_backlog.filter(active=True) 
        print(f">>> ==== SWIMLANE: {cards} === <<<") 
        grouped_cards[swimlane] = cards
    uncategorized_cards = CORE_HSDB.objects.filter(board=item, swimlane=None, active=True)
    grouped_cards[none_swimlane] = uncategorized_cards
    print(f">>> === {uncategorized_cards} === <<<")
    return grouped_cards

def card_metrics_update(value_type, pk, board_id):
    return_info = {}
    cfdData = []
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)

    item_class = Board
    column_class = BoardColumns
    obj = get_object_or_404(model_class, pk=pk)
    item = get_object_or_404(item_class, id=board_id)

    board_columns = None
    board_columns_first = None
    try:
        board_columns = column_class.objects.filter(board=item, active=True, deleted=False).order_by('position')
        board_columns_first = column_class.objects.filter(board=item, active=True, deleted=False).first()
        #print(f">>>>>>>>>>>>>>>>>>>>> BOARD COLUMNS FIRST {board_columns_first}")
    except column_class.DoesNotExist:
        board_columns = None
        #print(f">>>> BoardColumns is null for {item}")
    lc_model_class = model_name.lower()
    lc_item_class = "board"
    column_class = "BoardColumns"
    val_lookup = {lc_model_class: obj}
    item_lookup = {lc_item_class: item}
    context = {}
    newtodolist = CORE_HSDB.objects.filter(active=True, **val_lookup, **item_lookup , parent=None).order_by('position')
    newtodolist_count = newtodolist.count()
    board_columns_details = BoardColumns.objects.filter(board=item, active=True, deleted=False)
    # CARD METRICS ***************
    cycle_time_columns = BoardColumns.objects.filter(board=item,cycle_time_column=True)
    average_cycle_time = 0
    average_lead_time = 0
    total_lead_time = 0
    total_cycle_time = 0
    num_cards = len(newtodolist)
    #>>>>> ==== card time_spent display
    for card in newtodolist:
        card.time_spent_by_column = {
            column: card.cardmovement.filter(target_column=column).aggregate(Sum('time_spent')).get('time_spent__sum')
            for column in board_columns_details
        }
        card.total_time_spent = sum(
            (time_value.seconds if time_value else 0)  # Convert to seconds, handle None
            for time_value in card.time_spent_by_column.values()
        )

        card.cycle_time = sum(
            card.time_spent_by_column[column].total_seconds()
            for column in board_columns_details
            if column in cycle_time_columns and card.time_spent_by_column[column] is not None
        )
        total_cycle_time += card.cycle_time
        total_lead_time += card.total_time_spent
        if num_cards != 0:
            average_lead_time = timedelta(seconds=total_lead_time / num_cards)
            average_cycle_time = timedelta(seconds=total_cycle_time / num_cards)
    print(f"****************** Avg LT {average_lead_time} **** ")
    print(f"****************** Avg CT {average_cycle_time} **** ")


    ### average throughput for last 14days
    from datetime import datetime

    # Calculate the start and end dates for the last 14 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=14)

    # Query completed cards within the last 14 days
    completed_cards = newtodolist.filter(
        cardmovement__target_column__title__iexact='Done',
        cardmovement__time_exited__range=(start_date, end_date)
    ).distinct()

    # Calculate throughput
    throughput_last_14_days = completed_cards.count()

    ### average wip for the last 14days 
    # Calculate the start and end dates for the last 14 days
    end_date = timezone.now()
    start_date = end_date - timedelta(days=14)

    # Get a list of all unique dates within the last 14 days
    date_range = [start_date + timedelta(days=i) for i in range(15)]  # Including the end date

    average_wip = 0
    total_wip_count = 0

    for date in date_range[:-1]:  # Exclude the end date from calculations
        next_date = date_range[date_range.index(date) + 1]

        # Count cards that were in progress (WIP) on the current date
        wip_count = newtodolist.filter(
            cardmovement__source_column__title__iexact='WIP',
            cardmovement__time_entered__range=(date, next_date)
        ).distinct().count()

        total_wip_count += wip_count

    # Calculate average WIP
    average_wip = total_wip_count / len(date_range[:-1])


    # ----- CFD
    from datetime import datetime
    import matplotlib.pyplot as plt
    # Calculate start_date and end_date for the last 14 days
    # start_date = datetime(2023, 8, 17)
    # end_date = datetime(2023, 9, 2)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=14)
    columns = None
    dates = None
    card_counts_by_date = None
    time_interval = timedelta(days=1)  # Daily intervals
    # Print the calculated dates for verification
    print("Start Date:", start_date)
    print("End Date:", end_date)

    # Check if there's any card movement data for the specified columns and cards
    has_data = any(
        CardMovement.objects.filter(target_column__title=column, card__board=item).exists()
        for column in board_columns_details
    )
    cfd_display = False
    if not has_data:
        print("No data available for the specified columns and cards.")
    else:
        data = []
        current_date = start_date
        while current_date <= end_date:
            card_counts = {
                column.title: CardMovement.objects.filter(
                    time_entered__lte=current_date,
                    target_column=column,
                ).values('card').distinct().count()
                for column in board_columns_details
            }
            #print(f">>>>>> CARD COUNTS: {card_counts}")
            # Calculate the count of cards in the backlog that are not in cardmovement
            ## experiement ***** with backlog count addition or first column that is missing

            ## experiment ***** end
            # Create a new dictionary to hold the data for the current date
            day_data = {
                'date': current_date,
                'card_counts': card_counts
            }
            #print(f">>> === {day_data} === <<<")
            data.append(day_data)
            
            current_date += time_interval
        # Prepare data for plotting
        columns = [column.title for column in board_columns_details]
        dates = [item['date'] for item in data]
        card_counts_by_date = [item['card_counts'] for item in data]
        transposed_card_counts = list(zip(*[d.values() for d in card_counts_by_date]))
      
        #
        #
        # cfdData testing / sending the data 
        #
        #

        # Prepare data for plotting
        columns = [column.title for column in board_columns_details]
        dates = [item['date'] for item in data]
        card_counts_by_date = [item['card_counts'] for item in data]

        # Initialize cfdData
        

        # # Iterate through the data
        # for date, card_counts in zip(dates, card_counts_by_date):
        #     # Initialize cfdItem with date
        #     cfdItem = {'date': date}

        #     # Update the counts for each column dynamically
        #     print(f">>> === TESTIN1: {card_counts_by_date} === <<<")
        #     for column_title, count in zip(columns, card_counts):
        #         print(f">>> === TESTING: {column_title} ==> {count} === <<<")
        #         try:
        #             count = int(count)  # Try to convert to an integer
        #         except (ValueError, TypeError):
        #             count = 0  # Set to zero if conversion fails

        #         cfdItem[column_title] = count
        # Iterate through the data
        for date, card_counts in zip(dates, card_counts_by_date):
            # Initialize cfdItem with date
            cfdItem = {'date': date}

            # Update the counts for each column dynamically based on index
            for column_title in columns:
                count = card_counts.get(column_title, 0)
                #print(f">>> === TESTING: {column_title} ==> {count} === <<<")
                cfdItem[column_title] = count

            cfdData.append(cfdItem)
        # Initialize a new list to store the modified data
        transformed_cfdData = []
        # Iterate through the data and transform it
        for item in cfdData:
            # Extract the date as a string
            date_str = item['date'].strftime('%Y-%m-%d')

            # Create a new item with the date as a string
            transformed_item = {'date': date_str}

            # Copy relevant columns to the new item
            transformed_item.update({key: value for key, value in item.items() if key in columns})

            # Append the transformed item to the list
            transformed_cfdData.append(transformed_item)

        cfdData = transformed_cfdData

        # Plot the Cumulative Flow Diagram as an area graph
        plt.figure(figsize=(10, 6))
        plt.stackplot(dates, transposed_card_counts, labels=columns, alpha=0.7)
        plt.xlabel('Date')
        plt.ylabel('Card Counts')
        plt.title('Cumulative Flow Diagram')
        plt.xticks(rotation=45)
        plt.legend(loc='upper left')

        # Adjust y-axis limits based on card counts
        min_card_count = min([min(card_counts.values()) for card_counts in card_counts_by_date])
        max_card_count = max([max(card_counts.values()) for card_counts in card_counts_by_date])
        plt.ylim(min_card_count, max_card_count)

        # Adjust figure margins
        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.15, top=0.9)  # Adjust these values as needed

        # Save the image
        import os
        image_filename = 'cfd_plot.png'
        image_relative_path = os.path.join('img', image_filename)  # Relative path within static/img
        image_path = os.path.join(settings.STATICFILES_DIRS[0], image_relative_path)

        try:
            plt.savefig(image_path)
            print("Image saved successfully.")
            cfd_display = True
        except Exception as e:
            print("Error saving image:", e)

    # prepare return info
    return_info['average_cycle_time'] = average_cycle_time
    return_info['average_lead_time'] = average_lead_time
    return_info['average_wip'] = average_wip

    return_info['dates'] = average_wip
    return_info['columns'] = average_wip
    return_info['card_counts_by_date'] = average_wip

    return_info['cfd_display'] = cfd_display
    return_info['throughput_last_14_days'] = throughput_last_14_days
    return_info['newtodolist'] = newtodolist

    #print(f">>> === TESTING4: {cfdData} === <<<")
    return_info['cfdData'] = cfdData

    return return_info




# kanban board
@login_required(login_url='login')
@check_board_permissions_type('view')
def table_view(request, value_type, pk, board_id):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    item_class = Board
    column_class = BoardColumns
    obj = get_object_or_404(model_class, pk=pk)
    item = get_object_or_404(item_class, id=board_id)
    board_columns = None
    board_columns_first = None
    swimlane = Swimlane.objects.filter(active=True, board=item)
    try:
        board_columns = column_class.objects.filter(board=item, active=True, deleted=False).order_by('position')
        board_columns_first = column_class.objects.filter(board=item, active=True, deleted=False).first()
    except column_class.DoesNotExist:
        board_columns = None
    lc_model_class = model_name.lower()
    lc_item_class = "board"
    column_class = "BoardColumns"
    val_lookup = {lc_model_class: obj}
    item_lookup = {lc_item_class: item}
    context = {}
    newtodolist = CORE_HSDB.objects.filter(active=True, **val_lookup, **item_lookup , parent=None).order_by('position')
    newtodolist_count = newtodolist.count()
    form = CORE_HSDB_Form(request.user)
    url_ref = reverse('table_view', args=[model_name, pk, board_id])

    # experiment 1 card count
    board_columns_details = BoardColumns.objects.filter(board=item, active=True, deleted=False)

    card_count_details = {}
    for column in board_columns_details:
        col_obj = BoardColumns.objects.get(id=column.id)
        card_count_details[column.id] = CORE_HSDB.objects.filter(**val_lookup, 
                                            **item_lookup, column=col_obj).count()

    column_policy_details = {}
    for column in board_columns_details:
        col_obj = BoardColumns.objects.get(id=column.id)
        column_policy_details[column.id] = convert_to_ul_li(col_obj.policies)


    # board_history
    board_history = BoardHistory.objects.filter(board=item).last()
    # pagination
    newtodolist = CORE_HSDB.objects.filter(active=True, **val_lookup, **item_lookup ,
                                            parent=None).order_by('position', 'swimlane')
    newtodolist_count = newtodolist.count()
   
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
    if model_class is not None:
        if request.method == 'POST':
            newtodolist = None
            newtodolist_count = 0
            action = request.POST.get('action')
            if action == "Search/Clear":
                query = request.POST.get('title')
                if query:
                    newtodolist = CORE_HSDB.objects.filter(
                            Q(title__icontains=query) |
                            Q(description__icontains=query)).filter(**item_lookup)
                    newtodolist_count = newtodolist.count()
                    paginated_items = newtodolist
                    print(f">>>>>>>>>>>> PRINTING SEARCH: {newtodolist} ==> {newtodolist_count}")
                    for ntdl in newtodolist:
                        print(f"===> CHECKING {ntdl.title} {ntdl.board.title}")
                else:
                    newtodolist = CORE_HSDB.objects.filter(active=True, **val_lookup, **item_lookup , parent=None).order_by('position', 'swimlane')
                    newtodolist_count = newtodolist.count()
                if query is None:
                    query = ''
                
            else: 
                form = CORE_HSDB_Form(request.user, current_parent_id=None, data=request.POST)
                if form.is_valid():
                    workitemtype = form.cleaned_data['workitemtype']           
                    setattr(form.instance, value_type.lower(), obj)
                    form.instance.author = request.user
                    setattr(form.instance, lc_item_class, item)
                    setattr(form.instance, "column", board_columns_first) #setting the card to first column in board]
                    card = form.save()
                    ## first column 
                    CardMovement.objects.create(card=card,
                                    source_column=board_columns_first, target_column=board_columns_first, 
                                    author=request.user)

                    newtodolist = CORE_HSDB.objects.filter(active=True, **val_lookup, **item_lookup , parent=None).order_by('position',  'swimlane')
                    newtodolist_count = newtodolist.count()
                    print(f">>>>>>>>>>>> PRINTING CHECK ***: {newtodolist} ==> {newtodolist_count}")   
                    return redirect(url_ref)
                else:
                    print(f"form is invalid {form}")
        
        context = {'newtodolist': newtodolist,'form':form, 
                'newtodolist_count': newtodolist_count,
                'object': obj, 'value_type': value_type,
                'pk': pk, 'item': item, 'board_columns': board_columns,
                'card_count_details':card_count_details,
                'column_policy_details':column_policy_details,
                'board_history': board_history, 
                'pagination':selected_pagination, 'paginated_items': paginated_items, 
                'pagination_on': pagination_on,
                'swimlane': swimlane}
        #table_view
        return render(request, 'app_xpresskanban/boards/table_view.html', context)

# HELPER FUNCTION LINE/LIST
def convert_to_ul_li(text_with_newlines):
    lines = text_with_newlines.split('\n')
    if not lines:
        return ''  # Return an empty string if there are no lines
    
    ul_li_elements = '<ul>' + ''.join(f'<li>{line}</li>' for line in lines) + '</ul>'
    return ul_li_elements   

# ops_project ==> ops_value
#
#
# Board :: Table View Bulk Operations
#
#
@login_required(login_url='login')
@check_board_permissions_type('edit')
def ops_kanban(request, value_type, pk, board_id):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    item_class = Board
    obj = get_object_or_404(model_class, pk=pk)
    item = get_object_or_404(item_class, id=board_id)
    if model_class is not None:
        if request.method == 'POST':
            form_data = request.POST
            selected_project_ids = request.POST.getlist('project_box')        
            bulk_ops = form_data.get('bulk_project_ops')
            pagination = form_data.get('pagination')
            bulk_ops = form_data.get('bulk_project_ops')
            if bulk_ops == "bulk_delete":
                for id in selected_project_ids:
                    print(f">>> === BULK DELETE: {id} {item_class} === <<<")
                    CORE_HSDB.objects.filter(id=id).update(active=False, deleted=False,  author=request.user)
            if bulk_ops == "bulk_change":
                for id in selected_project_ids:
                    CORE_HSDB.objects.filter(id=id).update(active=False, deleted=False,  author=request.user)
            elif bulk_ops == "bulk_done":
                for id in selected_project_ids:
                    CORE_HSDB.objects.filter(id=id).update(done=True,  author=request.user)
            print(f">>>>>>>>>>>.FORM. {bulk_ops} is bulk_ops, pagination {pagination}")
            context = {'bulk_ops': bulk_ops, 'pagination': pagination, 
                       'selected_project_ids':selected_project_ids,
                       'object': obj, 'value_type': value_type,
                        'pk': pk, 'item': item}
            return render(request, 'app_xpresskanban/boards/bulk_ops_table_view.html', context)

# kanban board columns CRUD
@login_required(login_url='login')
@check_board_permissions_type('edit')
def kanban_board_columns(request, value_type, pk, board_id):
    model_name = value_type
    model_class = None
    item_class = Board
    column_class = BoardColumns

    model_class = get_model_class(model_name)
    obj = get_object_or_404(model_class, pk=pk)
    item = get_object_or_404(item_class, id=board_id)
    #col = get_object_or_404(column_class, board=item)
    
    lc_model_class = model_name.lower()
    lc_item_class = "board"
    val_lookup = {lc_model_class: obj}
    item_lookup = {lc_item_class: item}
    context = {}

    newtodolist = column_class.objects.filter(active=True, board=item).order_by('position')
    newtodolist_count = newtodolist.count()
    form = BoardColumnsForm()
    url_ref = reverse('kanban_board_columns', args=[model_name, pk, board_id])
    if model_class is not None:
        if request.method == 'POST':
            form = BoardColumnsForm(request.POST)
            if form.is_valid():                
                form.instance.author = request.user
                setattr(form.instance, lc_item_class, item)
                form.save()
                newtodolist_count = newtodolist.count()
                return redirect(url_ref)
            else:
                print(f"form is invalid {form}")
    context = {'newtodolist': newtodolist,'form':form, 
                'newtodolist_count': newtodolist_count,
                'object': obj, 'value_type': value_type,
                'pk': pk, 'item': item}
    return render(request, 'app_xpresskanban/boards/kanban_board_columns.html', context)

# kanban board columns CRUD
@login_required(login_url='login')
@check_board_permissions_type('edit')
def kanban_board_buffer_columns(request, value_type, pk, board_id, column_id):
    model_name = value_type
    model_class = None
    item_class = Board
    column_class = BoardColumns
    buffer_column_class = BoardBufferColumns

    model_class = get_model_class(model_name)
    obj = get_object_or_404(model_class, pk=pk)
    item = get_object_or_404(item_class, id=board_id)
    board_columns_ref = get_object_or_404(column_class, id=column_id)
    #col = get_object_or_404(column_class, board=item)
    
    lc_model_class = model_name.lower()
    lc_item_class = "board"
    lc_board_columns_class = "board_columns"
    val_lookup = {lc_model_class: obj}
    item_lookup = {lc_item_class: item}
    context = {}

    newtodolist = buffer_column_class.objects.filter(active=True, board_columns=board_columns_ref).order_by('position')
    newtodolist_count = newtodolist.count()
    form = BoardBufferColumnsForm()
    url_ref = reverse('kanban_board_buffer_columns', args=[model_name, pk, board_id, column_id])
    if model_class is not None:
        if request.method == 'POST':
            form = BoardBufferColumnsForm(request.POST)
            if form.is_valid():                
                form.instance.author = request.user
                setattr(form.instance, lc_board_columns_class, board_columns_ref)
                form.save()
                newtodolist_count = newtodolist.count()
                return redirect(url_ref)
            else:
                print(f"form is invalid {form}")
    context = {'newtodolist': newtodolist,'form':form, 
                'newtodolist_count': newtodolist_count,
                'object': obj, 'value_type': value_type,
                'pk': pk, 'item': item, 'column':board_columns_ref}
    return render(request, 'app_xpresskanban/boards/board_buffer_columns.html', context)


from django.db import transaction
# ---USEDCURRENTLY----
@login_required(login_url='login')
def ajax_board_updated(request):
    ajax_data = ""
    if request.method == 'POST':
        print("AJAX TEST START ------ NEW ONE")
        value_type = request.POST['value_type']  
        pk = int(request.POST['pk'])   
        board_id = int(request.POST['board_id'])
        print(f" >>>> inputs received from ajax req: vt {value_type} pk: {pk} board_id: {board_id}")
        model_class = get_model_class(value_type)
        lc_value_type = value_type.lower()
        obj = get_object_or_404(model_class, pk=pk)
        item = get_object_or_404(Board, id=board_id)       
        val_lookup = {lc_value_type: obj}
        item_lookup = {"board": item}
        item_state = request.POST['item_state']    
        item_state = item_state.replace('"','')
        item_details = item_state.split('_')
        print(item_details)
        col_id = item_details[0]
        task_id = item_details[1]
        
        ## Updating the card and cardmovement
        card_before = CORE_HSDB.objects.get(id=task_id)
        src_column = card_before.column
        dst_column = BoardColumns.objects.get(id=col_id)        
        time_entered = timezone.now()
        # Update the card's column
        CORE_HSDB.objects.filter(id=task_id).update(column=dst_column)
        # Calculate time_spent and create/update CardMovement entry
        if src_column != dst_column:
            print(f"GOOD Source and Destination column not same: {src_column.title} != {dst_column.title}")
            cardmovement = CardMovement.objects.filter(card=card_before).last()
            if cardmovement:
                print(f">>>> {cardmovement.card.title} ==> last movement is ===> {cardmovement.source_column} ==> {cardmovement.target_column}")
                cardmovement.time_exited = timezone.now()
                cardmovement.time_spent = cardmovement.time_exited - cardmovement.time_entered
                cardmovement.author = request.user
                cardmovement.save()
                print(f">>>> ======= UPDATED THE LAST COLUMN'S time exited")
            else:
                print(f"====> NoTE: No last card movement detected, so it is a new card entry")
            CardMovement.objects.create(card=card_before,
                                    source_column=src_column, target_column=dst_column, author=request.user)

        else:
            print(f"Source and Destination column same: {src_column.title} == {dst_column.title}")
            
        
    print(f'Now the state will change to {col_id} {src_column.title} for {task_id}')
    print("AJAX TEST COMPLETE")   
    response_data = {
            'success': True,
        }
    json =  JsonResponse(response_data)
    return json

# ajax_sorted_kanban_board
@login_required(login_url='login')
def ajax_sorted_kanban_board(request):   
    value_type = request.POST['value_type']  
    pk = int(request.POST['pk'])   
    board_id = int(request.POST['board_id'])
    model_class = get_model_class(value_type)
    obj = model_class.objects.get(id=pk)
    if request.method == 'POST':
        ajax_data = request.POST['sorted_list_data']
        print(f">>>> AJAX TEST NOW: {ajax_data}")
        new_data = ajax_data.replace("[",'')
        new_data = new_data.replace("]",'')
        sorted_list = new_data.split(",")
        seq = 1
        print(f">>>> AJAX TEST NOW1: {sorted_list}")
        for item in sorted_list:
            str = item.replace('"','')
            print(f">>>>>>>>>>> AJAX STRING CHECK: >>{str}<<")
            if str == "": 
                continue
            position = str.split('_')
            print(f">>>>>>>>>>>>>>>>> IDENTIFY {item} ==> {str} ==> {position}")
            CORE_HSDB.objects.filter(pk=position[0]).update(position=seq)
            seq = seq + 1
        context = {'page': 'Sorted Value', 
                   'active_tab': 'sorted_value',
                   'value_type': value_type,
                   'pk': pk,
                   'object': obj,
                   'item': item,
                   'ajax_data': ajax_data}
        json =  JsonResponse({'success':'Updated!'})
        return json


# views.py
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
#@csrf_exempt
def update_task_column(request, task_id, column_id):
     if request.method == 'POST':
        print("AJAX CHECKBOX METHOD TEST: update_task_column")
        ajax_data = request.POST['checkbox_data']
        checkbox_details = ajax_data.split('_')
        checkbox_id = checkbox_details[0]
        checkbox_position = checkbox_details[1]
        checkbox_status = strip_tags(checkbox_details[2])
        try:
            task = CORE_HSDB.objects.get(id=task_id)
            column = BoardColumns.objects.get(id=column_id)

            # Check if WIP limit reached
            tasks_in_status = CORE_HSDB.objects.filter(column=column)
            if column.wip_limit == 0 or tasks_in_status.count() < column.wip_limit:
                task.column = column
                task.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'WIP limit reached for this status.'})
        except (CORE_HSDB.DoesNotExist, BoardColumns.DoesNotExist):
            return JsonResponse({'success': False})
@login_required(login_url='login')
def ajaxupdate_task_column(request):
    print(f">>>>> AJAX UPDATE TASK MY COLUMN === this is test")
    if request.method == 'POST':
        print("AJAX CHECKBOX METHOD TEST")
        ajax_data = request.POST['checkbox_data']
        print(f">>>>>>>>>>> AJAX DATA {ajax_data}")
        checkbox_details = ajax_data.split('/')
        checkbox_id = checkbox_details[0]
        checkbox_val1 = checkbox_details[1]
        checkbox_val2 = strip_tags(checkbox_details[2])
        print(f">>>>>>>>>> ID: {checkbox_id} VAL1 {checkbox_val1} VAL2 {checkbox_val2}")
        column_obj = BoardColumns.objects.get(id=checkbox_val2)
        print(f">>>>>>> COLUMN OBJ {column_obj.title}")
        obj = CORE_HSDB.objects.filter(id=checkbox_val1).update(column=column_obj)

        response_data = {}
        response_data['result'] = obj

        return JsonResponse(response_data)
    context = {}
    return render(request, 'app_xpresskanban/boards/ajaxupdate.html', context)


@login_required(login_url='login')
@check_board_permissions_type('edit')
def edit_column(request, value_type, pk, board_id, column_id):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    item_class = Board
    column_class = BoardColumns
    url_ref = reverse('kanban_board_columns', args=[model_name, pk, board_id])
    column = None
    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        item = get_object_or_404(item_class,id=board_id)
        try:
            column = column_class.objects.get(id=column_id)
        except (BoardColumns.DoesNotExist):
            print(f"Column does not exists")
        form = BoardColumnsForm(instance=item)
        if request.method == 'POST':
            form = BoardColumnsForm(request.POST, instance=column)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect(url_ref)
            else:
                print(f">>>>> FORM IS INVALID: {form}")
        else:
            form = BoardColumnsForm(instance=column)
        context = {'page': 'Edit ' + model_name,'form': form, model_name: obj
                   ,'value_type': value_type, 'object': obj, 'item': item, 
                   'column': column}
        return render(request, 
                      'app_xpresskanban/boards/edit_column.html', context)
    else:
        # Handle invalid model name
        return redirect('kanban_home')  # Redirect to a proper error page or other handling

@login_required(login_url='login')
@check_board_permissions_type('edit')
def edit_buffer_column(request, value_type, pk, board_id, column_id, buffer_id):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    item_class = Board
    column_class = BoardColumns
    buffer_column_class = BoardBufferColumns
    url_ref = reverse('kanban_board_buffer_columns', args=[model_name, pk, board_id, column_id])
    column = None
    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        item = get_object_or_404(item_class,id=board_id)
        try:
            buffer_column = buffer_column_class.objects.get(id=buffer_id)
        except (BoardBufferColumns.DoesNotExist):
            print(f"Column does not exists")
        form = BoardBufferColumnsForm(instance=buffer_column)
        if request.method == 'POST':
            form = BoardBufferColumnsForm(request.POST, instance=buffer_column)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect(url_ref)
            else:
                print(f">>>>> FORM IS INVALID: {form}")
        else:
            form = BoardBufferColumnsForm(instance=buffer_column)
        context = {'page': 'Edit ' + model_name,'form': form, model_name: obj
                   ,'value_type': value_type, 'object': obj, 'item': item, 
                   'column': column, 'buffer_column':buffer_column}
        return render(request, 
                      'app_xpresskanban/boards/edit_buffer_column.html', context)
    else:
        # Handle invalid model name
        return redirect('kanban_home')  # Redirect to a proper error page or other handling    
   
@login_required(login_url='login')
@check_board_permissions_type('edit')
def delete_column(request, value_type, pk, board_id, column_id):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    url_ref = reverse('kanban_board_columns', args=[model_name, pk, board_id])
    item_class = Board
    column_class = BoardColumns
    column = None
    try:
       column = column_class.objects.get(id=column_id)
    except (BoardColumns.DoesNotExist):
        print(f">>>> BOARD COLUMNNS -- does not exists for {column_id}")
    item = get_object_or_404(item_class,id=board_id)
    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        context = {'value_type': value_type, model_name: obj, 'object': obj, 'item': item,
                   'column': column}
        if request.method == 'POST':
            column_class.objects.filter(id=column_id).update(active=False, author=request.user)     
            return redirect(url_ref)
        return render(request, 'app_xpresskanban/boards/delete_column_confirm.html', context)
    else:
        # Handle invalid model name
        return redirect('kanban_home')  # Redirect to a proper error page or other handling
    
@login_required(login_url='login')
@check_board_permissions_type('edit')
def delete_buffer_column(request, value_type, pk, board_id, column_id, buffer_id):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    url_ref = reverse('kanban_board_columns', args=[model_name, pk, board_id])
    item_class = Board
    column_class = BoardColumns
    buffer_column_class = BoardBufferColumns
    column = get_object_or_404(BoardColumns, id=column_id)
    buffer_column = None
    try:
       buffer_column = buffer_column_class.objects.get(id=buffer_id)
    except (BoardBufferColumns.DoesNotExist):
        print(f">>>> BOARD COLUMNNS -- does not exists for {column_id}")
    item = get_object_or_404(item_class,id=board_id)
    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        context = {'value_type': value_type, model_name: obj, 'object': obj, 'item': item,
                   'column': column, 'buffer_column':buffer_column}
        if request.method == 'POST':
            buffer_column_class.objects.filter(id=buffer_id).update(active=False, author=request.user)     
            return redirect(url_ref)
        return render(request, 'app_xpresskanban/boards/delete_buffer_column_confirm.html', context)
    else:
        # Handle invalid model name
        return redirect('kanban_home')  # Redirect to a proper error page or other handling
    
@login_required(login_url='login')
def sorted_board_columns(request, value_type, pk, board_id):   
    model_class = get_model_class(value_type)
    obj = model_class.objects.get(id=pk)
    if request.method == 'POST':
        ajax_data = request.POST['sorted_list_data']
        new_data = ajax_data.replace("[",'')
        new_data = new_data.replace("]",'')
        sorted_list = new_data.split(",")
        seq = 1
        for item in sorted_list:
            str = item.replace('"','')
            position = str.split('_')
            BoardColumns.objects.filter(pk=position[0]).update(position=seq)
            seq = seq + 1
        context = {'page': 'Sorted Value', 
                   'active_tab': 'sorted_value',
                   'value_type': value_type,
                   'pk': pk,
                   'object': obj,
                   'item': item,
                   'ajax_data': ajax_data}
        return render(request, 'app_xpresskanban/boards/kanban_board_columns.html',context)
    
@login_required(login_url='login')
def sorted_board_buffer_columns(request, value_type, pk, board_id, column_id):   
    model_class = get_model_class(value_type)
    obj = model_class.objects.get(id=pk)
    if request.method == 'POST':
        ajax_data = request.POST['sorted_list_data']
        new_data = ajax_data.replace("[",'')
        new_data = new_data.replace("]",'')
        sorted_list = new_data.split(",")
        seq = 1
        for item in sorted_list:
            str = item.replace('"','')
            position = str.split('_')
            BoardBufferColumns.objects.filter(pk=position[0]).update(position=seq)
            seq = seq + 1
        context = {'page': 'Sorted Value', 
                   'active_tab': 'sorted_value',
                   'value_type': value_type,
                   'pk': pk,
                   'object': obj,
                   'item': item,
                   'ajax_data': ajax_data}
        return render(request, 'app_xpresskanban/boards/kanban_board_buffer_columns.html',context)

#
#
# Kanban: Swimlanes (landing page / listing)
#
#
@login_required(login_url='login')
@check_board_permissions_type('view')
def kanban_swimlanes(request, value_type, pk, board_id):
    model_name = value_type
    model_class = None
    item_class = Board
    column_class = BoardColumns
    swimlane_class = Swimlane

    model_class = get_model_class(model_name)
    obj = get_object_or_404(model_class, pk=pk)
    item = get_object_or_404(item_class, id=board_id)
    #col = get_object_or_404(column_class, board=item)
    
    lc_model_class = model_name.lower()
    lc_item_class = "board"
    lc_swimlane_class = "swimlane"
    val_lookup = {lc_model_class: obj}
    item_lookup = {lc_item_class: item}
    context = {}

    newtodolist = swimlane_class.objects.filter(active=True, board=item).order_by('position')
    newtodolist_count = newtodolist.count()
    form = SwimlaneForm()
    url_ref = reverse('kanban_swimlanes', args=[model_name, pk, board_id])
    if model_class is not None:
        if request.method == 'POST':
            form = SwimlaneForm(request.POST)
            if form.is_valid():                
                form.instance.author = request.user
                setattr(form.instance, lc_item_class, item)
                form.save()
                newtodolist_count = newtodolist.count()
                return redirect(url_ref)
            else:
                print(f"form is invalid {form}")
    context = {'newtodolist': newtodolist,'form':form, 
                'newtodolist_count': newtodolist_count,
                'object': obj, 'value_type': value_type,
                'pk': pk, 'item': item}
    return render(request, 'app_xpresskanban/boards/kanban_swimlanes.html', context)

#
#
# edit
#
#
@login_required(login_url='login')
@check_board_permissions_type('edit')
def edit_swimlane(request, value_type, pk, board_id, sl_id):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    item_class = Board
    column_class = BoardColumns
    swimlane_class = Swimlane
    url_ref = reverse('kanban_swimlanes', args=[model_name, pk, board_id])
    swimlane = None
    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        item = get_object_or_404(item_class,id=board_id)
        try:
            swimlane = swimlane_class.objects.get(id=sl_id)
        except (Swimlane.DoesNotExist):
            print(f"Column does not exists")
        form = SwimlaneForm(instance=item)
        if request.method == 'POST':
            form = SwimlaneForm(request.POST, instance=swimlane)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect(url_ref)
            else:
                print(f">>>>> FORM IS INVALID: {form}")
        else:
            form = SwimlaneForm(instance=swimlane)
        context = {'page': 'Edit ' + model_name,'form': form, model_name: obj
                   ,'value_type': value_type, 'object': obj, 'item': item, 
                   'swimlane': swimlane}
        return render(request, 
                      'app_xpresskanban/boards/edit_swimlane.html', context)
    else:
        # Handle invalid model name
        return redirect('kanban_home')  # Redirect to a proper error page or other handling
    
#
#
# delete
#
#
@login_required(login_url='login')
@check_board_permissions_type('edit')
def delete_swimlane(request, value_type, pk, board_id, sl_id):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    url_ref = reverse('kanban_swimlanes', args=[model_name, pk, board_id])
    item_class = Board
    column_class = BoardColumns
    swimlane_class = Swimlane
    column = None
    try:
       swimlane = swimlane_class.objects.get(id=sl_id)
    except (Swimlane.DoesNotExist):
        print(f">>>> BOARD COLUMNNS -- does not exists for {sl_id}")
    item = get_object_or_404(item_class,id=board_id)
    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        context = {'value_type': value_type, model_name: obj, 'object': obj, 'item': item,
                   'swimlane': swimlane}
        if request.method == 'POST':
            swimlane_class.objects.filter(id=sl_id).update(active=False, author=request.user)     
            return redirect(url_ref)
        return render(request, 'app_xpresskanban/boards/delete_swimlane_confirm.html', context)
    else:
        # Handle invalid model name
        return redirect('kanban_home')  # Redirect to a proper error page or other handling
    
#
#
# sorted
#
#
@login_required(login_url='login')
def sorted_swimlanes(request, value_type, pk, board_id):   
    model_class = get_model_class(value_type)
    obj = model_class.objects.get(id=pk)
    if request.method == 'POST':
        ajax_data = request.POST['sorted_list_data']
        new_data = ajax_data.replace("[",'')
        new_data = new_data.replace("]",'')
        sorted_list = new_data.split(",")
        seq = 1
        for item in sorted_list:
            str = item.replace('"','')
            position = str.split('_')
            Swimlane.objects.filter(pk=position[0]).update(position=seq)
            seq = seq + 1
        context = {'page': 'Sorted Value', 
                   'active_tab': 'sorted_value',
                   'value_type': value_type,
                   'pk': pk,
                   'object': obj,
                   'item': item,
                   'ajax_data': ajax_data}
        return render(request, 'app_xpresskanban/boards/kanban_swimlanes.html',context)
    


#
#
# Kanban/Boards/TableView/Restore:ShowDeletedItems
#
#
@login_required(login_url='login')
@check_board_permissions_type('edit')
def restore_show_deleted_cards(request, value_type, pk, board_id):
    model_name = value_type
    model_class = None
    item_count = 0
    model_class = get_model_class(model_name)
    item_class = Board
    obj = get_object_or_404(model_class, pk=pk)
    item = get_object_or_404(item_class, id=board_id)
    lc_model_class = model_name.lower()
    lc_item_class = "board"
    val_lookup = {lc_model_class: obj}
    item_lookup = {lc_item_class: item}
    column_class = BoardColumns
    context = {}
    board_columns = None
    board_columns_first = None
    swimlane = Swimlane.objects.filter(active=True, board=item)
    try:
        board_columns = column_class.objects.filter(board=item, active=True, deleted=False).order_by('position')
        board_columns_first = column_class.objects.filter(board=item, active=True, deleted=False).first()
    except column_class.DoesNotExist:
        board_columns = None
    newtodolist = CORE_HSDB.objects.filter(active=False, deleted=False, **val_lookup, 
                            **item_lookup , parent=None).order_by('position', 'swimlane')
    newtodolist_count = newtodolist.count()
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
    print(f">>> === CHECKIGN RESTORE SHOW DC: {newtodolist} and count: {newtodolist_count} === <<<")
    if model_class is not None:
        context = {'page': 'Show Deleted Cards'}
        # here we list all projects deleted and restore
        item_class = Board
        newtodolist = CORE_HSDB.objects.filter(active=False, deleted=False).order_by('position')
        newtodolist_count = newtodolist.count()
        form = CORE_HSDB_Form(request.user)
        url_ref = reverse('table_view', args=[model_name, pk, item.id])
        if request.method == 'POST':
            form = CORE_HSDB_Form(request.user, request.POST)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                item_count = newtodolist.count()
                return redirect(url_ref)
            else:
                print(f"form is invalid {form}")
        context = {'newtodolist': newtodolist,'form':form, 
                   'newtodolist_count': newtodolist_count, 'value_type': value_type,
                   'pk': pk, 'item_count': item_count,'item':item,
                   'object': obj, 
                    'pagination':selected_pagination, 'paginated_items': paginated_items, 
                    'pagination_on': pagination_on,
                    'swimlane': swimlane, 'board_columns': board_columns}
        return render(request, 'app_xpresskanban/boards/show_deleted_cards.html', context)
    
### bulk operations ###
@login_required(login_url='login')
@check_board_permissions_type('edit')
def bulk_restore_deleted_cards(request, value_type, pk, board_id):
    model_name = value_type
    model_class = None
    model_class = get_model_class(model_name)
    item_class = Board
    obj = get_object_or_404(model_class, pk=pk)
    item = get_object_or_404(item_class, id=board_id)
    lc_model_class = model_name.lower()
    lc_item_class = "board"
    val_lookup = {lc_model_class: obj}
    item_lookup = {lc_item_class: item}
    column_class = BoardColumns
    board_columns = None
    board_columns_first = None
    swimlane = Swimlane.objects.filter(active=True, board=item)
    if model_class is not None:
        if request.method == 'POST':
            form_data = request.POST
            selected_project_ids = request.POST.getlist('restore_project_box')      
            bulk_ops = form_data.get('bulk_project_ops')
            print(f">>> === BULK OPS: {bulk_ops} selectedids: {selected_project_ids} === <<<")
            if bulk_ops == "bulk_restore":
                for id in selected_project_ids:
                    CORE_HSDB.objects.filter(id=id).update(active=True,  author=request.user)
                    print(f">>> === BULK OPS: {bulk_ops} ==>  {id} === <<<")
            elif bulk_ops == "bulk_not_done":
                for id in selected_project_ids:
                    CORE_HSDB.objects.filter(id=id).update(done=False,  author=request.user)
            elif bulk_ops == "bulk_delete_permanently":
                for id in selected_project_ids:
                    CORE_HSDB.objects.filter(id=id).update(active=False, deleted=True,  author=request.user)
            pagination = form_data.get('pagination')
            print(f">>> === FORM. {bulk_ops} is bulk_ops, pagination {pagination} === <<<")
            context = {'bulk_ops': bulk_ops, 'pagination': pagination, 
                    'selected_project_ids':selected_project_ids, 'value_type': value_type}
        return render(request, 'app_xpresskanban/boards/bulk_restore_deleted_cards.html', context)