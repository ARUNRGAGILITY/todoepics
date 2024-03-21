from .all_view_imports import *
from ..forms_ext.canvas_forms import *
from django.core.serializers import serialize
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.apps import apps


def parse_marked_data(data_str):
    """
    Parses strings of the form '1,2,3' or '1='tag1'/2='tag2'' into a Python dictionary.
    """
    if data_str is None:
        return {}
    if '=' in data_str:
        # For marked_rows_with_tag
        return dict(item.split('=') for item in data_str.split('/'))
    else:
        # For marked_steps_with_star
        return [int(item) for item in data_str.split(',') if item.isdigit()]


def parse_marked_rows_to_list(data_str):
    """Parse the marked_rows_with_tag string into a list of (row, tag) for easier use in templates."""
    row_tags = []
    if data_str:
        for part in data_str.split('/'):
            key, value = part.split('=')
            row_tags.append((int(key), value.strip("'")))
    return row_tags
# # Example usage in your view before passing to the template
# dev_transformation_canvas = DevTransformationCanvas.objects.get(id=some_id)
# marked_steps_with_star = parse_marked_data(dev_transformation_canvas.marked_steps_with_star)
# marked_rows_with_tag = parse_marked_data(dev_transformation_canvas.marked_rows_with_tag)

# # Add these to your context
# context = {
#     'marked_steps_with_star': marked_steps_with_star,
#     'marked_rows_with_tag': marked_rows_with_tag,
#     # Include other context variables as needed
# }


def create_current_state_snapshot(dtc_id, dvs_id):
    # Fetch the specific DevValueStream and its ValueStreamSteps
    devvaluestream = get_object_or_404(DevValueStream, id=dvs_id, active=True)
    steps = ValueStreamSteps.objects.filter(devvaluestream=devvaluestream, active=True)    
    # Serialize to JSON
    dev_value_stream_json = serialize('json', [devvaluestream, ])
    steps_json = serialize('json', steps)    
    snapshot_data = {
        'dev_value_stream': json.loads(dev_value_stream_json),
        'value_stream_steps': json.loads(steps_json),
    }
    
    # Create or update the CurrentStateDTC with the serialized data
    CurrentStateDTC.objects.update_or_create(
        dtc_id=dtc_id,
        defaults={'snapshot': snapshot_data}
    )

def create_future_state_snapshot(dtc_id, dvs_id):
    # Fetch the specific DevValueStream and its ValueStreamSteps
    devvaluestream = get_object_or_404(DevValueStream, id=dvs_id, active=True)
    steps = ValueStreamSteps.objects.filter(devvaluestream=devvaluestream, active=True)    
    # Serialize to JSON
    dev_value_stream_json = serialize('json', [devvaluestream, ])
    steps_json = serialize('json', steps)    
    snapshot_data = {
        'dev_value_stream': json.loads(dev_value_stream_json),
        'value_stream_steps': json.loads(steps_json),
    }
    
    # Create or update the CurrentStateDTC with the serialized data
    FutureStateDTC.objects.update_or_create(
        dtc_id=dtc_id,
        defaults={'snapshot': snapshot_data}
    )

@login_required(login_url='login')
def ops_trx_add_canvas(request, id):
    if request.method == 'POST':
        form = OpsTransformationCanvasForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('ops_trx_list_canvas', id=id)  # Redirect to the listing view
    else:
        form = OpsTransformationCanvasForm()
    context = {'form': form, 'id':id,}
    template_file = f"{app_name}/_cafe/canvas/transformation/add_ops_canvas.html"
    return render(request, template_file, context)

@login_required(login_url='login')
def ops_trx_list_canvas(request, id):
    canvases = OpsTransformationCanvas.objects.filter(active=True)
    # Ensure the OpsValueStream exists and get it
    opsvaluestream = get_object_or_404(OpsValueStream, pk=id,active=True)    
    # Filter canvases by the OpsValueStream's ID
    canvases = OpsTransformationCanvas.objects.filter(opsvaluestream=opsvaluestream, active=True)
    context = {
        'canvases': canvases,
        'opsvaluestream': opsvaluestream,
        'id':id,
    }
    template_file = f"{app_name}/_cafe/canvas/transformation/list_ops_canvases.html"
    return render(request, template_file, context)

@login_required(login_url='login')
def ops_trx_view_canvas(request, canvas_id):
    canvas = get_object_or_404(OpsTransformationCanvas, id=canvas_id)
    id = canvas.opsvaluestream.id
    steps = canvas.opsvaluestream.steps.filter(active=True).order_by('position')
    first_step = steps.first()
    last_step = steps.last()
    formatted_created_at = canvas.created_at.strftime("%d/%m/%Y %H:%M:%S")
    formatted_updated_at = canvas.updated_at.strftime("%d/%m/%Y %H:%M:%S")
    context = {'canvas': canvas, 'id':id,
               'first_step': first_step, 
               'last_step':last_step, 
               'first_step_id': first_step.id, 
               'last_step_id': last_step.id,               
               'formatted_created_at': formatted_created_at,
               'formatted_updated_at': formatted_updated_at}
    template_file = f"{app_name}/_cafe/canvas/transformation/view_ops_canvas.html"
    return render(request, template_file, context)

@login_required(login_url='login')
def ops_trx_edit_canvas(request, canvas_id):
    canvas = get_object_or_404(OpsTransformationCanvas, id=canvas_id)
    id = canvas.opsvaluestream.id
    if request.method == 'POST':
        form = OpsTransformationCanvasForm(request.POST, instance=canvas)
        if form.is_valid():
            form.save()
            return redirect('ops_trx_list_canvas', id=id)
    else:
        form = OpsTransformationCanvasForm(instance=canvas)

    context = {'form': form, 'id':id,}
    template_file = f"{app_name}/_cafe/canvas/transformation/edit_ops_canvas.html"
    return render(request, template_file, context)

@login_required(login_url='login')
def ops_trx_delete_canvas(request, canvas_id):
    canvas = get_object_or_404(OpsTransformationCanvas, id=canvas_id)
    id = canvas.opsvaluestream.id
    if request.method == 'POST':
        canvas = get_object_or_404(OpsTransformationCanvas, id=canvas_id)
        canvas.active = False
        canvas.deleted = False
        canvas.save()
        return redirect('ops_trx_list_canvas', id=id)

    context = {'canvas': canvas,  'id':id,}
    template_file = f"{app_name}/_cafe/canvas/transformation/delete_ops_canvas.html"
    return render(request, template_file, context)


# Dev
@login_required(login_url='login')
def dev_trx_add_canvas(request, id):
    if request.method == 'POST':
        form = DevTransformationCanvasForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            dtc = form.save()
            # current & future state saved 
            create_current_state_snapshot(dtc.id, id)
            create_future_state_snapshot(dtc.id, id)
            return redirect('dev_trx_list_canvas', id=id)  # Redirect to the listing view
    else:
        form = DevTransformationCanvasForm()
    context = {'form': form, 'id':id,}
    template_file = f"{app_name}/_cafe/canvas/transformation/add_dev_canvas.html"
    return render(request, template_file, context)

@login_required(login_url='login')
def dev_trx_list_canvas(request, id):
    canvases = DevTransformationCanvas.objects.filter(active=True)
    # Ensure the DevValueStream exists and get it
    devvaluestream = get_object_or_404(DevValueStream, pk=id,active=True)    
    # Filter canvases by the DevValueStream's ID
    canvases = DevTransformationCanvas.objects.filter(devvaluestream=devvaluestream, active=True)
    context = {
        'canvases': canvases,
        'devvaluestream': devvaluestream,
        'id':id,      
    }
    template_file = f"{app_name}/_cafe/canvas/transformation/list_dev_canvases.html"
    return render(request, template_file, context)

@login_required(login_url='login')
def dev_trx_view_canvas(request, canvas_id):
    canvas = get_object_or_404(DevTransformationCanvas, id=canvas_id)
    id = canvas.devvaluestream.id
    steps = canvas.devvaluestream.steps.filter(active=True).order_by('position', 'created_at')
    first_step = steps.first()
    last_step = steps.last()
    
    for step in steps:
        print(f">>> === |||| >>>{step.id}==> {step.position} ==> {step.name} |||| === <<<")
    # Check if first_step or last_step is not None before accessing id
    if first_step:
        first_step_id = first_step.id
    else:
        # Handle the case where there is no first step
        first_step_id = None  # Or set a default value or take another action
    if last_step:
        last_step_id = last_step.id
    else:
        # Handle the case where there is no last step
        last_step_id = None 
    #print(f">>> === |||| first_step {first_step.id} {first_step}  last_step {last_step.id} {last_step} |||| === <<<")
    formatted_created_at = canvas.created_at.strftime("%d/%m/%Y %H:%M:%S")
    formatted_updated_at = canvas.updated_at.strftime("%d/%m/%Y %H:%M:%S")    
    steps_count = steps.count()   
    # We are going to send the steps 4 columns per row
    # for displaying like post-it notes
    columns_per_row = 4
    rows = [steps[i:i + columns_per_row] for i in range(0, len(steps), columns_per_row)]
    #print(f">>> === |||| MARKED STARS {canvas.marked_steps_with_star} |||| === <<<")
    marked_steps_with_star = parse_marked_data(canvas.marked_steps_with_star)
    marked_rows_with_tag = parse_marked_data(canvas.marked_rows_with_tag)
    marked_rows_with_tag_to_list = parse_marked_rows_to_list(canvas.marked_rows_with_tag)
    # Zip the rows with their corresponding tags
    # Example of combining rows with their corresponding tags
    rows_with_tags = [(row, next((tag for index, tag in marked_rows_with_tag_to_list if index == row_index + 1), '')) for row_index, row in enumerate(rows)]


    # snapshot check
    current_state_dtc = get_object_or_404(CurrentStateDTC, dtc=canvas)
    # The snapshot data is already a Python dict if accessed directly
    snapshot_data = current_state_dtc.snapshot
    # Accessing parts of the snapshot
    dev_value_stream_data = snapshot_data.get('dev_value_stream', [])
    value_stream_steps_data = snapshot_data.get('value_stream_steps', [])
    cdtc_rows = [value_stream_steps_data[i:i + columns_per_row] for i in range(0, len(value_stream_steps_data), columns_per_row)]
    # marked_steps_with_star = ""
    # marked_rows_with_tag = ""
    context = {'canvas': canvas, 'id':id,
               'first_step': first_step, 
               'last_step':last_step, 
               'first_step_id': first_step_id, 
               'last_step_id': last_step_id,      
               'formatted_created_at': formatted_created_at,
               'formatted_updated_at': formatted_updated_at, 
               'rows': rows,
               'cdtc_rows': cdtc_rows,
               'rows_with_tags': rows_with_tags,
               'marked_steps_with_star':marked_steps_with_star,
               'marked_rows_with_tag':marked_rows_with_tag,
               'marked_rows_with_tag_to_list':marked_rows_with_tag_to_list,
               'dev_value_stream_data':dev_value_stream_data[0],
               'value_stream_steps_data':value_stream_steps_data,}
    template_file = f"{app_name}/_cafe/canvas/transformation/view_dev_canvas.html"
    return render(request, template_file, context)



@login_required(login_url='login')
def dev_trx_view_canvas_we(request, canvas_id):
    canvas = get_object_or_404(DevTransformationCanvas, id=canvas_id)
    id = canvas.devvaluestream.id
    steps = canvas.devvaluestream.steps.filter(active=True).order_by('position', 'created_at')
    first_step = steps.first()
    last_step = steps.last()
    
    for step in steps:
        print(f">>> === |||| >>>{step.id}==> {step.position} ==> {step.name} |||| === <<<")
    # Check if first_step or last_step is not None before accessing id
    if first_step:
        first_step_id = first_step.id
    else:
        # Handle the case where there is no first step
        first_step_id = None  # Or set a default value or take another action
    if last_step:
        last_step_id = last_step.id
    else:
        # Handle the case where there is no last step
        last_step_id = None 
    #print(f">>> === |||| first_step {first_step.id} {first_step}  last_step {last_step.id} {last_step} |||| === <<<")
    formatted_created_at = canvas.created_at.strftime("%d/%m/%Y %H:%M:%S")
    formatted_updated_at = canvas.updated_at.strftime("%d/%m/%Y %H:%M:%S")    
    steps_count = steps.count()   
    # We are going to send the steps 4 columns per row
    # for displaying like post-it notes
    columns_per_row = 4
    rows = [steps[i:i + columns_per_row] for i in range(0, len(steps), columns_per_row)]
    #print(f">>> === |||| MARKED STARS {canvas.marked_steps_with_star} |||| === <<<")
    marked_steps_with_star = parse_marked_data(canvas.marked_steps_with_star)
    marked_rows_with_tag = parse_marked_data(canvas.marked_rows_with_tag)
    marked_rows_with_tag_to_list = parse_marked_rows_to_list(canvas.marked_rows_with_tag)
    # Zip the rows with their corresponding tags
    # Example of combining rows with their corresponding tags
    rows_with_tags = [(row, next((tag for index, tag in marked_rows_with_tag_to_list if index == row_index + 1), '')) for row_index, row in enumerate(rows)]


    # snapshot check
    current_state_dtc = get_object_or_404(CurrentStateDTC, dtc=canvas)
    # The snapshot data is already a Python dict if accessed directly
    snapshot_data = current_state_dtc.snapshot
    # Accessing parts of the snapshot
    dev_value_stream_data = snapshot_data.get('dev_value_stream', [])
    value_stream_steps_data = snapshot_data.get('value_stream_steps', [])
    cdtc_rows = [value_stream_steps_data[i:i + columns_per_row] for i in range(0, len(value_stream_steps_data), columns_per_row)]
    # marked_steps_with_star = ""
    # marked_rows_with_tag = ""
    context = {'canvas': canvas, 'id':id,
               'first_step': first_step, 
               'last_step':last_step, 
               'first_step_id': first_step_id, 
               'last_step_id': last_step_id,      
               'formatted_created_at': formatted_created_at,
               'formatted_updated_at': formatted_updated_at, 
               'rows': rows,
               'cdtc_rows': cdtc_rows,
               'rows_with_tags': rows_with_tags,
               'marked_steps_with_star':marked_steps_with_star,
               'marked_rows_with_tag':marked_rows_with_tag,
               'marked_rows_with_tag_to_list':marked_rows_with_tag_to_list,
               'dev_value_stream_data':dev_value_stream_data[0],
               'value_stream_steps_data':value_stream_steps_data,}
    template_file = f"{app_name}/_cafe/canvas/transformation/view_dev_canvas_with_efficiency.html"
    return render(request, template_file, context)


from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa


@login_required(login_url='login')
def dev_trx_view_canvas_pdf(request, canvas_id):
    canvas = get_object_or_404(DevTransformationCanvas, id=canvas_id)
    id = canvas.devvaluestream.id
    steps = canvas.devvaluestream.steps.filter(active=True).order_by('position', 'created_at')
    first_step = steps.first()
    last_step = steps.last()
    
    for step in steps:
        print(f">>> === |||| >>>{step.id}==> {step.position} ==> {step.name} |||| === <<<")
    # Check if first_step or last_step is not None before accessing id
    if first_step:
        first_step_id = first_step.id
    else:
        # Handle the case where there is no first step
        first_step_id = None  # Or set a default value or take another action
    if last_step:
        last_step_id = last_step.id
    else:
        # Handle the case where there is no last step
        last_step_id = None 
    #print(f">>> === |||| first_step {first_step.id} {first_step}  last_step {last_step.id} {last_step} |||| === <<<")
    formatted_created_at = canvas.created_at.strftime("%d/%m/%Y %H:%M:%S")
    formatted_updated_at = canvas.updated_at.strftime("%d/%m/%Y %H:%M:%S")    
    steps_count = steps.count()   
    # We are going to send the steps 4 columns per row
    # for displaying like post-it notes
    columns_per_row = 4
    rows = [steps[i:i + columns_per_row] for i in range(0, len(steps), columns_per_row)]
    #print(f">>> === |||| MARKED STARS {canvas.marked_steps_with_star} |||| === <<<")
    marked_steps_with_star = parse_marked_data(canvas.marked_steps_with_star)
    marked_rows_with_tag = parse_marked_data(canvas.marked_rows_with_tag)
    marked_rows_with_tag_to_list = parse_marked_rows_to_list(canvas.marked_rows_with_tag)
    # Zip the rows with their corresponding tags
    # Example of combining rows with their corresponding tags
    rows_with_tags = [(row, next((tag for index, tag in marked_rows_with_tag_to_list if index == row_index + 1), '')) for row_index, row in enumerate(rows)]


    # snapshot check
    current_state_dtc = get_object_or_404(CurrentStateDTC, dtc=canvas)
    # The snapshot data is already a Python dict if accessed directly
    snapshot_data = current_state_dtc.snapshot
    # Accessing parts of the snapshot
    dev_value_stream_data = snapshot_data.get('dev_value_stream', [])
    value_stream_steps_data = snapshot_data.get('value_stream_steps', [])
    cdtc_rows = [value_stream_steps_data[i:i + columns_per_row] for i in range(0, len(value_stream_steps_data), columns_per_row)]
    # marked_steps_with_star = ""
    # marked_rows_with_tag = ""
    context = {'canvas': canvas, 'id':id,
               'first_step': first_step, 
               'last_step':last_step, 
               'first_step_id': first_step_id, 
               'last_step_id': last_step_id,      
               'formatted_created_at': formatted_created_at,
               'formatted_updated_at': formatted_updated_at, 
               'rows': rows,
               'cdtc_rows': cdtc_rows,
               'rows_with_tags': rows_with_tags,
               'marked_steps_with_star':marked_steps_with_star,
               'marked_rows_with_tag':marked_rows_with_tag,
               'marked_rows_with_tag_to_list':marked_rows_with_tag_to_list,
               'dev_value_stream_data':dev_value_stream_data[0],
               'value_stream_steps_data':value_stream_steps_data,}
    template_file = f"{app_name}/_cafe/canvas/transformation/view_dev_canvas_pdf.html"
    #return render(request, template_file, context)
     # Render your template with context data
    html = render_to_string(template_file, {'some': 'context'})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(
       html, dest=response)

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




@login_required(login_url='login')
def dev_trx_view_agree_on_canvas(request, canvas_id):
    marked_steps_with_star = None
    marked_rows_with_tag = None
    canvas = get_object_or_404(DevTransformationCanvas, id=canvas_id)
    id = canvas.devvaluestream.id
    steps = canvas.devvaluestream.steps.filter(active=True).order_by('position')
    first_step = steps.first()
    last_step = steps.last()
    #print(f">>> === |||| first_step {first_step.id} {first_step}  last_step {last_step.id} {last_step} |||| === <<<")
    formatted_created_at = canvas.created_at.strftime("%d/%m/%Y %H:%M:%S")
    formatted_updated_at = canvas.updated_at.strftime("%d/%m/%Y %H:%M:%S")    
    steps_count = steps.count()   
    # We are going to send the steps 4 columns per row
    # for displaying like post-it notes
    columns_per_row = 4
    rows = [steps[i:i + columns_per_row] for i in range(0, len(steps), columns_per_row)]    
    marked_steps_with_star = parse_marked_data(canvas.marked_steps_with_star)
    marked_rows_with_tag = parse_marked_data(canvas.marked_rows_with_tag)
    marked_rows_with_tag_to_list = parse_marked_rows_to_list(canvas.marked_rows_with_tag)
    rows_with_tags = [(row, next((tag for index, tag in marked_rows_with_tag_to_list if index == row_index + 1), '')) for row_index, row in enumerate(rows)]
    ## post method to save the star and row tags
    if request.method == 'POST':
        # Process form submission
        records_selected = []
        row_tags = {}
        
        for key, value in request.POST.items():
            if key.startswith('record_'):
                # Extract the record ID and mark as selected
                record_id = key.split('_')[1]
                records_selected.append(record_id)
            elif key.startswith('row_') and key.endswith('_tag'):
                # Extract the row number and associated tag
                row_number = key.split('_')[1]
                row_tags[row_number] = value
                #print(f">>> === |||| {row_tags}==> {value} |||| === <<<")
        canvas = get_object_or_404(DevTransformationCanvas, id=canvas_id)
        marked_steps_with_star = ','.join(records_selected)
        marked_rows_with_tag = '/'.join([f"{key}='{value}'" for key, value in row_tags.items()])
        canvas.marked_steps_with_star = marked_steps_with_star
        canvas.marked_rows_with_tag = marked_rows_with_tag
        canvas.active = True
        canvas.save()
        #print(f">>> === |||| records_selected: {records_selected} rowtags: {row_tags} , {canvas.marked_steps_with_star} |||| === <<<")
        
        marked_steps_with_star = parse_marked_data(canvas.marked_steps_with_star)
        marked_rows_with_tag = parse_marked_data(canvas.marked_rows_with_tag)
        marked_rows_with_tag_to_list = parse_marked_rows_to_list(canvas.marked_rows_with_tag)
        return redirect('dev_trx_view_canvas', canvas_id=canvas_id)
    context = {'canvas': canvas, 'id':id,
               'first_step': first_step, 
               'last_step':last_step, 
               'first_step_id': first_step.id, 
               'last_step_id': last_step.id,      
               'formatted_created_at': formatted_created_at,
               'formatted_updated_at': formatted_updated_at, 'rows': rows,
               'rows_with_tags': rows_with_tags,
               'marked_steps_with_star':marked_steps_with_star,
               'marked_rows_with_tag':marked_rows_with_tag,
               'marked_rows_with_tag_to_list':marked_rows_with_tag_to_list,}
    template_file = f"{app_name}/_cafe/canvas/transformation/view_agree_on_dev_canvas.html"
    return render(request, template_file, context)

@login_required(login_url='login')
def dev_trx_edit_canvas(request, canvas_id):
    canvas = get_object_or_404(DevTransformationCanvas, id=canvas_id)
    id = canvas.devvaluestream.id
    if request.method == 'POST':
        form = EditDevTransformationCanvasForm(request.POST, instance=canvas)
        if form.is_valid():
            form.save()
            return redirect('dev_trx_list_canvas', id=id)
    else:
        form = EditDevTransformationCanvasForm(instance=canvas)

    context = {'form': form, 'id':id,}
    template_file = f"{app_name}/_cafe/canvas/transformation/edit_dev_canvas.html"
    return render(request, template_file, context)

@login_required(login_url='login')
def dev_trx_delete_canvas(request, canvas_id):
    canvas = get_object_or_404(DevTransformationCanvas, id=canvas_id)
    id = canvas.devvaluestream.id
    if request.method == 'POST':
        canvas = get_object_or_404(DevTransformationCanvas, id=canvas_id)
        canvas.active = False
        canvas.deleted = False
        canvas.save()
        return redirect('dev_trx_list_canvas', id=id)

    context = {'canvas': canvas,  'id':id,}
    template_file = f"{app_name}/_cafe/canvas/transformation/delete_dev_canvas.html"
    return render(request, template_file, context)


def ajax_update_dtc_field(request):
    model_name = request.POST.get('model')
    field_name = request.POST.get('field')
    value = request.POST.get('value')
    idx = request.POST.get('id')
    object_id = request.POST.get('object_id')
    print(f">>> === AJAX UPDATE DTC FIELD === <<<")
    Model = apps.get_model('app_web', model_name)  # Update 'your_app_name'
    obj = None
    dvs_id = None
    if model_name == "ValueStreamSteps":
        dvs_id = request.POST.get('dev_id')
        dvs = get_object_or_404(DevValueStream, id=dvs_id, active=True)
        
        update_fields = {"name": value}
        obj = ValueStreamSteps.objects.filter(id=idx, devvaluestream=dvs).update(**update_fields)
    else:
        obj = Model.objects.get(id=idx)
        setattr(obj, field_name, value)
    print(f">>> === dev_id: {dvs_id}, obj: {obj}, model: {model_name}, field_name: {field_name}, value: {value}, id: {idx} object_id={object_id}, === <<<")
    obj.save()

    return JsonResponse({'success': True})

"""
# Example: Fetch the CurrentStateDTC for a specific DevTransformationCanvas
dtc_id = 1  # Assuming you know the DevTransformationCanvas ID
current_state_dtc = CurrentStateDTC.objects.get(dtc_id=dtc_id)

# The snapshot data is already a Python dict if accessed directly
snapshot_data = current_state_dtc.snapshot

# Accessing parts of the snapshot
dev_value_stream_data = snapshot_data.get('dev_value_stream', [])
value_stream_steps_data = snapshot_data.get('value_stream_steps', [])

# In your view
return render(request, 'your_template.html', {
    'dev_value_stream_data': dev_value_stream_data,
    'value_stream_steps_data': value_stream_steps_data,
})


# Example: Iterating over deserialized ValueStreamSteps data
for step in value_stream_steps_data:
    print(step['fields']['name'])  # Adjust accessing the 'fields' and 'name' based on your model structure


<h2>Value Stream Steps</h2>
<ul>
    {% for step in value_stream_steps_data %}
    <li>{{ step.fields.name }}</li>  <!-- Adjust based on your actual structure -->
    {% endfor %}
</ul>

---
dev value stream is access from the snapshot data
# Assuming you have the snapshot_data as previously described
dev_value_stream_data = snapshot_data.get('dev_value_stream', [])

# If there's only one DevValueStream in the snapshot or you're interested in the first one
if dev_value_stream_data:
    first_dev_value_stream = dev_value_stream_data[0]
    dev_value_stream_name = first_dev_value_stream['fields']['name']
    dev_value_stream_description = first_dev_value_stream['fields']['description']
    
    print(dev_value_stream_name, dev_value_stream_description)
    # Now you can use dev_value_stream_name and dev_value_stream_description as needed

"""