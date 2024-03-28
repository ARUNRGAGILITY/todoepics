from .common_import_for_views import *

# kanban board
@login_required(login_url='login')
@check_board_permissions_type('view')
def visual_board_dandd(request, value_type, pk, board_id):
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
    except column_class.DoesNotExist:
        board_columns = None
    lc_model_class = model_name.lower()
    lc_item_class = "board"
    column_class = "BoardColumns"
    val_lookup = {lc_model_class: obj}
    item_lookup = {lc_item_class: item}
    newtodolist = CORE_HSDB.objects.filter(active=True, **val_lookup, 
                            **item_lookup , parent=None).order_by('position', 'swimlane')
    newtodolist_count = newtodolist.count()
    form = CORE_HSDB_Form(request.user)
    board_columns_details = BoardColumns.objects.filter(board=item, active=True, deleted=False)

    card_count_details = {}
    for column in board_columns_details:
        col_obj = BoardColumns.objects.get(id=column.id)        
        card_count_details[column.id] = CORE_HSDB.objects.filter(
                **val_lookup,
                **item_lookup,
                column=col_obj, active=True,
            ).exclude(swimlane__title__iexact='Expedite').count()
    
    column_policy_details = {}
    for column in board_columns_details:
        col_obj = BoardColumns.objects.get(id=column.id)
        if col_obj.policies != "":
            column_policy_details[column.id] = convert_to_ul_li(col_obj.policies)
    url_ref = reverse('visual_board_dandd', args=[model_name, pk, board_id])
    swimlane = Swimlane.objects.filter(active=True, board=item)
    only_none_swimlane=True
    swimlane_titles = Swimlane.objects.filter(board=item, active=True).values('title').annotate(title_count=Count('title'))
    if swimlane_titles.filter(title_count__gt=0).exists():
        only_none_swimlane=False
    grouped_cards = group_cards(newtodolist, item)
    board_cards = CORE_HSDB.objects.filter(board=item,active=True).order_by('position')
    # processing POST method
    if model_class is not None:
        if request.method == 'POST':
            newtodolist = None
            newtodolist_count = 0
            action = request.POST.get('action')
            if action == "Add":
                form = CORE_HSDB_Form(request.user, current_parent_id=None, data=request.POST)
                initial_colum = "Start"
                if form.is_valid():
                    workitemtype = form.cleaned_data['workitemtype']           
                    setattr(form.instance, value_type.lower(), obj)
                    form.instance.author = request.user
                    setattr(form.instance, lc_item_class, item)
                    #setattr(form.instance, "column", initial_colum) 
                    form.instance.position = 0                   
                    card = form.save()

                    newtodolist = CORE_HSDB.objects.filter(active=True, **val_lookup, 
                                           **item_lookup , parent=None).order_by('position')
                    newtodolist_count = newtodolist.count()
                    return redirect(url_ref)
                else:
                    print(f"form is invalid {form}")

    # sending to view
    context = {'value_type': value_type,'object': obj, 'item':item,'columns':board_columns_first
               ,'only_none_swimlane':only_none_swimlane, 'grouped_cards': grouped_cards,
                 'board_cards': board_cards, 'board_columns': board_columns,
                 'newtodolist':newtodolist, 'newtodolist_count':newtodolist_count,
                 'swimlane':swimlane,
                 'form':form}
    return render(request,
                  "app_xpresskanban/mvp2_0/boards/visual_board_dndd.html",
                  context)


# kanban board
@login_required(login_url='login')
@check_board_permissions_type('view')
def visual_board_dandd_swimlanes(request, value_type, pk, board_id):
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
    except column_class.DoesNotExist:
        board_columns = None

    # counting the buffer columns for header colspan
    buffer_column_count = 0
    for bc in board_columns:
        buffer_column_count += bc.boardbuffercolumns_set.count()
    
    lc_model_class = model_name.lower()
    lc_item_class = "board"
    column_class = "BoardColumns"
    val_lookup = {lc_model_class: obj}
    item_lookup = {lc_item_class: item}
    newtodolist = CORE_HSDB.objects.filter(active=True, **val_lookup, 
                            **item_lookup , parent=None).order_by('position', 'swimlane')
    newtodolist_count = newtodolist.count()
    form = CORE_HSDB_Form(request.user)
    board_columns_details = BoardColumns.objects.filter(board=item, active=True, deleted=False)

    card_count_details = {}
    for column in board_columns_details:
        col_obj = BoardColumns.objects.get(id=column.id)        
        card_count_details[column.id] = CORE_HSDB.objects.filter(
                **val_lookup,
                **item_lookup,
                column=col_obj, active=True,
            ).exclude(swimlane__title__iexact='Expedite').count()
    
    column_policy_details = {}
    for column in board_columns_details:
        col_obj = BoardColumns.objects.get(id=column.id)
        if col_obj.policies != "":
            column_policy_details[column.id] = convert_to_ul_li(col_obj.policies)
    url_ref = reverse('visual_board_dandd_swimlanes', args=[model_name, pk, board_id])
    swimlane = Swimlane.objects.filter(active=True, board=item)
    only_none_swimlane=True
    swimlane_titles = Swimlane.objects.filter(board=item, active=True).values('title').annotate(title_count=Count('title'))
    if swimlane_titles.filter(title_count__gt=0).exists():
        only_none_swimlane=False
    grouped_cards = group_cards(newtodolist, item)
    grouped_cards_count = newtodolist_count
    board_cards = CORE_HSDB.objects.filter(board=item,active=True).order_by('position')
    if request.GET.get("blocked") != None:
        card_given_id = request.GET.get("blocked")
        print(f">>> === blocked given {card_given_id}=== <<<")
        card_read = CORE_HSDB.objects.get(id=card_given_id,active=True)
        card_read.block()
        card_read.save()
    elif request.GET.get("unblocked") != None:
        card_given_id = request.GET.get("unblocked")
        print(f">>> === unblocked given {card_given_id}=== <<<")
        card_read = CORE_HSDB.objects.get(id=card_given_id,active=True)
        card_read.unblock()
        card_read.save()
    else:
        bcard_y = 1
    # processing POST method
    if model_class is not None:
        if request.method == 'POST':
            newtodolist = None
            newtodolist_count = 0
            action = request.POST.get('action')
            if action == "Add":
                form = CORE_HSDB_Form(request.user, current_parent_id=None, data=request.POST)
                initial_colum = "Start"
                if form.is_valid():
                    workitemtype = form.cleaned_data['workitemtype']           
                    setattr(form.instance, value_type.lower(), obj)
                    form.instance.author = request.user
                    setattr(form.instance, lc_item_class, item)
                    #setattr(form.instance, "column", initial_colum) 
                    form.instance.position = 0                   
                    card = form.save()

                    newtodolist = CORE_HSDB.objects.filter(active=True, **val_lookup, 
                                           **item_lookup , parent=None).order_by('position')
                    newtodolist_count = newtodolist.count()
                    return redirect(url_ref)
                else:
                    print(f"form is invalid {form}")

    # sending to view
    # START CFD DATA PROCESSING 09092023953
    from datetime import date, datetime
    current_date = date.today()
    current_date.strftime('%Y-%m-%d')
    columns_with_counts = BoardColumns.objects.filter(
        board=item,
        active=True,
        deleted=False
    ).annotate(
        active_card_count=Count('column_backlog', filter=Q(column_backlog__active=True, column_backlog__deleted=False))
    )
    # Initialize the data array with the current date and counts for each column
    current_datetime = datetime.now()
    # Initialize the data dictionary with today's date and counts for each column
    cfd_date = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    cfd_date1 = current_datetime.strftime('%Y-%m-%d')
    cfd_data = {'date': cfd_date}
    for column in columns_with_counts:
        cfd_data[column.title] = column.active_card_count

    # Get the existing CFDData instance or create a new one if it doesn't exist
    existing_data = CFDData.objects.filter(board=item, date=cfd_date1).first()
    if existing_data:
        #print(f">>> === EXISTING DATA: {cfd_date1} ==> {existing_data.cfd_data} === <<<")
        existing_data = CFDData.objects.get(board=item, date=cfd_date1)
        existing_data.cfd_data = json.dumps(cfd_data)
        existing_data.save()
    else:
        #print(f">>> === NO DATA: {cfd_date1} ==>  === <<<")
        new_data = CFDData(board=item, date=cfd_date1, cfd_data=json.dumps(cfd_data))
        new_data.save()
    # === till this point working ok === #
    final_string = None
    cfd_data_records = CFDData.objects.filter(board=item).order_by('date')
    cfd_data_array = []
    for record in cfd_data_records:
        cfd_data_array.append(json.loads(record.cfd_data))
    cfd_display = True
    #print(f">>> === ********** FINAL STRING {cfd_data_array} ******** === <<<")
    # END CFD DATA PROCESSING
    context = {'value_type': value_type,'object': obj, 'item':item,'columns':board_columns_first
               ,'only_none_swimlane':only_none_swimlane, 'grouped_cards': grouped_cards,
               'grouped_cards_count':grouped_cards_count,
                 'board_cards': board_cards, 'board_columns': board_columns,
                 'buffer_column_count':buffer_column_count,
                 'newtodolist':newtodolist, 'newtodolist_count':newtodolist_count,
                 'swimlane':swimlane,'cfd_data': cfd_data_array,'cfd_display': cfd_display,
                 'form':form}
    return render(request,
                  "app_xpresskanban/mvp2_0/boards/visual_board_dndd_swimlanes.html",
                  context)

# HELPER FUNCTION LINE/LIST
############################################ ALL HELP/SUPPORT HERE ###############################
#
#
#
#
#
def get_cfd_data_for_days(item, no_of_days):
    from datetime import date, timedelta

    # Get the current date
    current_date = date.today()

    # Calculate yesterday's date by subtracting one day
    yesterday_date = current_date - timedelta(days=no_of_days)

    # Assuming you have a reference to the specific board 'item'
    board = item

    # Query to get a list of columns with counts of active cards within the specific board for yesterday's date
    columns_with_counts = BoardColumns.objects.filter(
        board=board,
        active=True,
        deleted=False,
        column_backlog__created_at__date=yesterday_date
    ).annotate(
        active_card_count=Count('column_backlog', filter=Q(column_backlog__active=True, column_backlog__deleted=False))
    )

    # Initialize the data array with yesterday's date and counts for each column
    cfd_str_yesterday = [{'date': yesterday_date.strftime('%Y-%m-%d'), **{column.title: column.active_card_count for column in columns_with_counts}}]
    cfd_str = cfd_str_yesterday + cfd_str_yesterday
    # Example: Print the array
    print(f">>> === ********** COMBINED {cfd_str} ******** === <<<")
    return cfd_str_yesterday


def convert_to_ul_li(text_with_newlines):
    lines = text_with_newlines.split('\n')
    if not lines:
        return ''  # Return an empty string if there are no lines
    
    ul_li_elements = '<ul>' + ''.join(f'<li>{line}</li>' for line in lines) + '</ul>'
    return ul_li_elements   


def group_cards(cards, item):
    swimlanes = Swimlane.objects.filter(active=True, board=item).order_by('position')
    grouped_cards = {}
    none_swimlane = None
    for swimlane in swimlanes:
        print(f">>> ==== SWIMLANE: {swimlane} board:{item} === <<<")
        cards = swimlane.swimlane_backlog.filter(active=True).order_by('position') 
        print(f">>> ==== SWIMLANE: {cards} === <<<") 
        grouped_cards[swimlane] = cards
    uncategorized_cards = CORE_HSDB.objects.filter(board=item, swimlane=None, active=True).order_by('position')
    grouped_cards[none_swimlane] = uncategorized_cards
    print(f">>> === {uncategorized_cards} === <<<")
    return grouped_cards

def replace_null_with_none(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = replace_null_with_none(value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = replace_null_with_none(item)
    elif data is None:
        return None
    elif data == "null":
        return None
    return data

############################################ ALL AJAX REQUESTS HERE ###############################
#
#
#
#
#
# ajax_sorted_kanban_board
@login_required(login_url='login')

def ajaxupdate_visual_board_dndd_swimlanes(request):   
    value_type = request.POST['value_type']  
    pk = int(request.POST['pk'])   
    board_id = int(request.POST['board_id'])
    model_class = get_model_class(value_type)
    obj = model_class.objects.get(id=pk)
    item = get_object_or_404(Board, id=board_id)    

    if request.method == 'POST':
        ajax_data = request.POST['data']
        print(f">>>> AJAX TEST NOW: {ajax_data}")
        print(f">>> === AJAX RECEIVED val {value_type}_id: {pk}, board_id: {board_id} === <<<")

        # processing the collected Data
        # testing the details
        # Get the JSON data from the request
         # Parse JSON data from the request body
        # Parse JSON data from the FormData
        collected_data_json = request.POST.get('data')
        #print(f"COLLECTED DATA : {collected_data_json}")
        collected_data = eval(collected_data_json)

        # Now you have access to the data in the 'collected_data' variable
        for item in collected_data:
            list_id = item['listId']
            list_data = item['listData']

            # Process the data as needed
            # print(f"===========================")
            # print("List ID:", list_id)
            #print("List Data:", list_data)
            # print(f"===========================")
            column_id = None
            column_details = None
            #column = BoardColumns.objects.get(id=column_id)
            column = None
            if list_id == "sortable_backlog":
                column = None
            else:
                column = BoardColumns.objects.get(id=list_id)
            position = 1
            for sub_list in list_data:
                if list_id == "sortable_backlog":
                    card = sub_list
                    swimlane = None      
                    update_card_movement(request, card, column)              
                    CORE_HSDB.objects.filter(id=card).update(column=None, position=position, swimlane_id=swimlane)
                else:
                     print(f">>> === {sub_list} === <<<")
                     card, swimlane = sub_list
                     if swimlane == 0:
                         swimlane = None
                     update_card_movement(request, card, column)   
                     CORE_HSDB.objects.filter(id=card).update(column=column, position=position, swimlane_id=swimlane)
                position = position + 1
                #print(f">>> === CARD & COLUMN UPDATED {column_id} ==> {card} === <<<")

        context = {'page': 'Sorted Value', 
                   'active_tab': 'sorted_value',
                   'value_type': value_type,
                   'pk': pk,
                   'object': obj,
                   'item': item,
                   'ajax_data': ajax_data}
        json =  JsonResponse({'success':'Updated!'})
        return json

# helper to update card movement
@login_required(login_url='login')
def update_card_movement(request,card_id, dst_column):
    #print(f">>> === COLUMN: **** {dst_column} **** === <<<")
    card_before_change = CORE_HSDB.objects.get(id=card_id)
    src_column = card_before_change.column
    if src_column != dst_column:
        #print(f"GOOD Source and Destination column not same: {src_column} != {dst_column}")
        cardmovement = CardMovement.objects.filter(card=card_before_change).last()
        if cardmovement:
            #print(f">>>> {cardmovement.card.title} ==> last movement is ===> {cardmovement.source_column} ==> {cardmovement.target_column}")
            cardmovement.time_exited = timezone.now()
            cardmovement.time_spent = cardmovement.time_exited - cardmovement.time_entered
            cardmovement.author = request.user
            cardmovement.save()
            #print(f">>> === UPDATED THE LAST COLUMN'S time exited === <<<")
        else:
            #print(f">>> ===  NOTE: No last card movement detected, so it is a new card entry === <<<")
            count = 1
        CardMovement.objects.create(card=card_before_change,
                                source_column=src_column, target_column=dst_column,
                                author=request.user)

    else:
        #print(f"Source and Destination column same: {src_column} == {dst_column}")
        count = 1

############################################ ALL AJAX REQUESTS HERE ###############################
#
#
#
#
#
# ajax_sorted_kanban_board
@login_required(login_url='login')

def ajaxupdate_visual_board_dndd(request):   
    value_type = request.POST['value_type']  
    pk = int(request.POST['pk'])   
    board_id = int(request.POST['board_id'])
    model_class = get_model_class(value_type)
    obj = model_class.objects.get(id=pk)
    item = get_object_or_404(Board, id=board_id)

    

    if request.method == 'POST':
        ajax_data = request.POST['data']
        print(f">>>> AJAX TEST NOW: {ajax_data}")
        print(f">>> === AJAX RECEIVED val {value_type}_id: {pk}, board_id: {board_id} === <<<")

        # processing the collected Data
        # testing the details
        # Get the JSON data from the request
         # Parse JSON data from the request body
        # Parse JSON data from the FormData
        collected_data_json = request.POST.get('data')
        print(f"COLLECTED DATA : {collected_data_json}")
        collected_data = eval(collected_data_json)

        # Now you have access to the data in the 'collected_data' variable
        for item in collected_data:
            list_id = item['listId']
            list_data = item['listData']

            # Process the data as needed
            print(f"===========================")
            print("List ID:", list_id)
            print("List Data:", list_data)
            print(f"===========================")
            column_details = list_id.split('_')
            column_id=column_details[1]
            if column_id == "backlog":
                column=None
            else:
                column = BoardColumns.objects.get(id=column_id)
            position = 1
            for card in list_data:
                if column_id == "backlog":
                    update_card_movement(request, card, column)    
                    CORE_HSDB.objects.filter(id=card).update(column=None, position=position)
                else:
                    update_card_movement(request, card, column)    
                    CORE_HSDB.objects.filter(id=card).update(column=column, position=position)
                position = position + 1
                print(f">>> === CARD & COLUMN UPDATED {column_id} ==> {card} === <<<")

        context = {'page': 'Sorted Value', 
                   'active_tab': 'sorted_value',
                   'value_type': value_type,
                   'pk': pk,
                   'object': obj,
                   'item': item,
                   'ajax_data': ajax_data}
        json =  JsonResponse({'success':'Updated!'})
        return json
