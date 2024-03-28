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
        # Add more mappings if needed
    }
    return model_classes.get(value_type)

@login_required(login_url='login')
def edit_card(request, value_type, pk, board_id, card_id):
    model_name = value_type
    model_class = get_model_class(value_type)
    obj = model_class.objects.get(id=pk)
    item = get_object_or_404(Board, id=board_id)
    card = get_object_or_404(CORE_HSDB, id=card_id)
    form = CORE_HSDB_Form(request.user, instance=card)
    board_columns = BoardColumns.objects.filter(board=item)
    # Card must have Valuetype, pk, boardid, cardid, cardobject
    url_ref = reverse('table_view', args=[value_type, pk, board_id])
    url_ref_table_view = reverse('table_view', args=[value_type, pk, board_id])
    url_ref_vsl = reverse('visual_board_dandd_swimlanes', args=[value_type, pk, board_id])
    url_ref_vsb = reverse('visual_board_dandd', args=[value_type, pk, board_id])
    url_ref_kb = reverse('kanban_board', args=[value_type, pk, board_id])
    if request.method == 'POST':
        from_which_url = request.GET.get('from', '')
        form = CORE_HSDB_Form(request.user, current_parent_id=None, data=request.POST, instance=card)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            if from_which_url == "vsl":
                return redirect(url_ref_vsl)
            elif from_which_url == "vsb":
                return redirect(url_ref_vsb)
            elif from_which_url == "tb":
                return redirect(url_ref_kb)
            elif from_which_url == "kb":
                return redirect(url_ref_kb)
            else:
                return redirect(url_ref)
   
    context = {'value_type': value_type, 'object': obj,
                'item': item, 'card':card, 'form': form,
                'board_columns': board_columns,
               }

    return render(request, "app_xpresskanban/cards/edit_card.html", context)

@login_required(login_url='login')
def mark_label(request, value_type, pk, board_id, card_id):
    model_name = value_type
    model_class = get_model_class(value_type)
    obj = model_class.objects.get(id=pk)
    item = get_object_or_404(Board, id=board_id)
    card = get_object_or_404(CORE_HSDB, id=card_id)
    form = CORE_HSDB_Form(request.user, instance=card)
    board_columns = BoardColumns.objects.filter(board=item)
    # check what is the details
    from_which_url = request.GET.get('from', '')
    what_label = request.GET.get('label', '')
    # Card must have Valuetype, pk, boardid, cardid, cardobject
    url_ref = reverse('table_view', args=[value_type, pk, board_id])
    url_ref_table_view = reverse('table_view', args=[value_type, pk, board_id])
    url_ref_vsl = reverse('visual_board_dandd_swimlanes', args=[value_type, pk, board_id])
    url_ref_vsb = reverse('visual_board_dandd', args=[value_type, pk, board_id])
    url_ref_kb = reverse('kanban_board', args=[value_type, pk, board_id])
    if what_label != "":
        if what_label.lower() == "none":
            CORE_HSDB.objects.filter(id=card_id).update(label='')
        else:
            CORE_HSDB.objects.filter(id=card_id).update(label=what_label)
    if request.method == 'POST':
        from_which_url = request.GET.get('from', '')
        what_label = request.GET.get('label', '')
        form = CORE_HSDB_Form(request.user, current_parent_id=None, data=request.POST, instance=card)
        if form.is_valid():
            form.instance.label = what_label
            form.instance.author = request.user
            form.save()
            if from_which_url == "vsl":
                return redirect(url_ref_vsl)
            elif from_which_url == "vsb":
                return redirect(url_ref_vsb)
            elif from_which_url == "tb":
                return redirect(url_ref_table_view)
            elif from_which_url == "kb":
                return redirect(url_ref_kb)
            else:
                return redirect(url_ref)
   
    context = {'value_type': value_type, 'object': obj,
                'item': item, 'card':card, 'form': form,
                'board_columns': board_columns,
               }
    if from_which_url == "vsl":
        return redirect(url_ref_vsl)
    elif from_which_url == "vsb":
        return redirect(url_ref_vsb)
    elif from_which_url == "tb":
        return redirect(url_ref_table_view)
    elif from_which_url == "kb":
        return redirect(url_ref_kb)
    else:
        return redirect(url_ref)
    #return render(request, "app_xpresskanban/cards/edit_card.html", context)


@login_required(login_url='login')
def view_card(request, value_type, pk, board_id, card_id):
    model_name = value_type
    model_class = get_model_class(value_type)
    obj = model_class.objects.get(id=pk)
    item = get_object_or_404(Board, id=board_id)
    card = get_object_or_404(CORE_HSDB, id=card_id)
    form = CORE_HSDB_Form(request.user, instance=card)
    board_columns = BoardColumns.objects.filter(board=item)
    # Card must have Valuetype, pk, boardid, cardid, cardobject

    context = {'value_type': value_type, 'object': obj,
                'item': item, 'card':card, 'form': form,
                'board_columns': board_columns,
               }

    return render(request, "app_xpresskanban/cards/view_card.html", context)

@login_required(login_url='login')
def delete_card(request, value_type, pk, board_id, card_id):
    model_name = value_type
    model_class = get_model_class(value_type)
    obj = model_class.objects.get(id=pk)
    item = get_object_or_404(Board, id=board_id)
    card = get_object_or_404(CORE_HSDB, id=card_id)
    form = CORE_HSDB_Form(request.user, instance=card)
    board_columns = BoardColumns.objects.filter(board=item)
    # Card must have Valuetype, pk, boardid, cardid, cardobject
    url_ref = reverse('table_view', args=[value_type, pk, board_id])
    from_which_url = request.GET.get('from', '')
    # Card must have Valuetype, pk, boardid, cardid, cardobject
    url_ref = reverse('table_view', args=[value_type, pk, board_id])
    url_ref_table_view = reverse('table_view', args=[value_type, pk, board_id])
    url_ref_vsl = reverse('visual_board_dandd_swimlanes', args=[value_type, pk, board_id])
    url_ref_vsb = reverse('visual_board_dandd', args=[value_type, pk, board_id])
    url_ref_kb = reverse('kanban_board', args=[value_type, pk, board_id])
    if request.method == 'POST':
        from_which_url = request.GET.get('from', '')
        CORE_HSDB.objects.filter(id=card_id).update(active=False, author=request.user) 
        if from_which_url == "vsl":
            return redirect(url_ref_vsl)
        elif from_which_url == "vsb":
            return redirect(url_ref_vsb)
        elif from_which_url == "tb":
            return redirect(url_ref_table_view)
        elif from_which_url == "kb":
            return redirect(url_ref_kb)
        else:
            return redirect(url_ref)
   
    context = {'value_type': value_type, 'object': obj,
                'item': item, 'card':card, 'form': form,
                'board_columns': board_columns,
               }

    return render(request, "app_xpresskanban/cards/delete_card.html", context)


@login_required(login_url='login')
def delete_card_sl(request, value_type, pk, board_id, card_id):
    model_name = value_type
    model_class = get_model_class(value_type)
    obj = model_class.objects.get(id=pk)
    item = get_object_or_404(Board, id=board_id)
    card = get_object_or_404(CORE_HSDB, id=card_id)
    form = CORE_HSDB_Form(request.user, instance=card)
    board_columns = BoardColumns.objects.filter(board=item)
    # Card must have Valuetype, pk, boardid, cardid, cardobject
    url_ref = reverse('visual_board_dandd_swimlanes', args=[value_type, pk, board_id])
    if request.method == 'POST':
        CORE_HSDB.objects.filter(id=card_id).update(active=False, author=request.user)     
        return redirect(url_ref)
   
    context = {'value_type': value_type, 'object': obj,
                'item': item, 'card':card, 'form': form,
                'board_columns': board_columns,
               }

    return render(request, "app_xpresskanban/cards/delete_card.html", context)




# views.py
from django.http import JsonResponse
@login_required(login_url='login')
def ajaxupdate_card(request):
    if request.method == 'POST':
        todo_id = request.POST.get('todo_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        column_id = request.POST.get('column')
        swimlane_id = request.POST.get('swimlane')
        done = request.POST.get('done')   
        save_field_done = False
        if done == "true":
            save_field_done=True

        print(f">>>> AJAXUPDATE_CARD testing... ID, title,description,columnid,done:{todo_id}, {title}, {description},{column_id},{done}")
        try:            
            todo = CORE_HSDB.objects.get(id=todo_id)
            src_column = todo.column # capture before update
            card_before = todo
            # Update the fields
            todo.title = title
            todo.description = description
            todo.column_id = column_id
            todo.swimlane_id = swimlane_id
            todo.done = save_field_done
            todo.save()
               
            # Update card movement here            
            dst_column = BoardColumns.objects.get(id=column_id)        
            time_entered = timezone.now()
            # Update the card's column
            CORE_HSDB.objects.filter(id=todo_id).update(column=dst_column)
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
                
            
            
            # end of card movement update
            return JsonResponse({'success': True})
        except CORE_HSDB.DoesNotExist:
            pass
    
    return JsonResponse({'success': False})


# board's column need to move to columns_views.py
@login_required(login_url='login')
def ajaxupdate_column(request):
    if request.method == 'POST':
        todo_id = request.POST.get('todo_id')
        cycle_time_column = request.POST.get('cycle_time_column')   
        save_field_done = False
        if cycle_time_column == "true":
            save_field_done=True

        print(f">>>> AJAXUPDATE_COLUMN:{todo_id},{cycle_time_column}")
        try:            
            todo = BoardColumns.objects.get(id=todo_id)
            # Update the fields
            print(f">>>>> {todo} ==> {todo.cycle_time_column}")
            todo.cycle_time_column = save_field_done
            todo.save()

            return JsonResponse({'success': True})
        except CORE_HSDB.DoesNotExist:
            pass
    
    return JsonResponse({'success': False})


# board's buffer column need to move to columns_views.py
@login_required(login_url='login')
def ajaxupdate_buffer_column(request):
    if request.method == 'POST':
        todo_id = request.POST.get('todo_id')
        cycle_time_column = request.POST.get('cycle_time_column')   
        save_field_done = False
        if cycle_time_column == "true":
            save_field_done=True

        #print(f">>>> AJAXUPDATE_BUFFER_COLUMN:{todo_id},{cycle_time_column}")
        try:            
            todo = BoardBufferColumns.objects.get(id=todo_id)
            # Update the fields
            #print(f">>>>> {todo} ==> {todo.cycle_time_column}")
            todo.cycle_time_column = save_field_done
            todo.save()

            return JsonResponse({'success': True})
        except CORE_HSDB.DoesNotExist:
            pass
    
    return JsonResponse({'success': False})
