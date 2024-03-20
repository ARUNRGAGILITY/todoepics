from .all_view_imports import *
from ..forms_ext.canvas_forms import *
from django.core.serializers import serialize
import json

def create_current_state_snapshot(dev_transformation_canvas_id, dvs_id):
    # Fetch the specific DevValueStream and its ValueStreamSteps
    devvaluestream = DevValueStream.objects.filter(id=dvs_id, active=True)
    steps = ValueStreamSteps.objects.filter(devvaluestream=devvaluestream)
    
    # Serialize to JSON
    dev_value_stream_json = serialize('json', dev_value_stream)
    steps_json = serialize('json', steps)
    
    snapshot_data = {
        'dev_value_stream': json.loads(dev_value_stream_json),
        'value_stream_steps': json.loads(steps_json),
    }
    
    # Create or update the CurrentStateDTC with the serialized data
    CurrentStateDTC.objects.update_or_create(
        dtc_id=dev_transformation_canvas_id,
        defaults={'snapshot': snapshot_data}
    )



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

def ops_trx_view_canvas(request, canvas_id):
    canvas = get_object_or_404(OpsTransformationCanvas, id=canvas_id)
    id = canvas.opsvaluestream.id
    steps = canvas.opsvaluestream.steps.filter(active=True).order_by('position')
    first_step = steps.first()
    last_step = steps.last()
    formatted_created_at = canvas.created_at.strftime("%d/%m/%Y %H:%M:%S")
    formatted_updated_at = canvas.updated_at.strftime("%d/%m/%Y %H:%M:%S")
    context = {'canvas': canvas, 'id':id,'first_step': first_step, 'last_step':last_step,
               'formatted_created_at': formatted_created_at,
               'formatted_updated_at': formatted_updated_at}
    template_file = f"{app_name}/_cafe/canvas/transformation/view_ops_canvas.html"
    return render(request, template_file, context)

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

def dev_trx_add_canvas(request, id):
    if request.method == 'POST':
        form = DevTransformationCanvasForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('dev_trx_list_canvas', id=id)  # Redirect to the listing view
    else:
        form = DevTransformationCanvasForm()
    context = {'form': form, 'id':id,}
    template_file = f"{app_name}/_cafe/canvas/transformation/add_dev_canvas.html"
    return render(request, template_file, context)


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

def dev_trx_view_canvas(request, canvas_id):
    canvas = get_object_or_404(DevTransformationCanvas, id=canvas_id)
    id = canvas.devvaluestream.id
    steps = canvas.devvaluestream.steps.filter(active=True).order_by('position')
    first_step = steps.first()
    last_step = steps.last()
    formatted_created_at = canvas.created_at.strftime("%d/%m/%Y %H:%M:%S")
    formatted_updated_at = canvas.updated_at.strftime("%d/%m/%Y %H:%M:%S")    
    steps_count = steps.count()   
    # We are going to send the steps 4 columns per row
    # for displaying like post-it notes
    columns_per_row = 4
    rows = [steps[i:i + columns_per_row] for i in range(0, len(steps), columns_per_row)]
    context = {'canvas': canvas, 'id':id,'first_step': first_step, 'last_step':last_step,
               'formatted_created_at': formatted_created_at,
               'formatted_updated_at': formatted_updated_at, 'rows': rows}
    template_file = f"{app_name}/_cafe/canvas/transformation/view_dev_canvas.html"
    return render(request, template_file, context)

def dev_trx_edit_canvas(request, canvas_id):
    canvas = get_object_or_404(DevTransformationCanvas, id=canvas_id)
    id = canvas.devvaluestream.id
    if request.method == 'POST':
        form = DevTransformationCanvasForm(request.POST, instance=canvas)
        if form.is_valid():
            form.save()
            return redirect('dev_trx_list_canvas', id=id)
    else:
        form = DevTransformationCanvasForm(instance=canvas)

    context = {'form': form, 'id':id,}
    template_file = f"{app_name}/_cafe/canvas/transformation/edit_dev_canvas.html"
    return render(request, template_file, context)


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
