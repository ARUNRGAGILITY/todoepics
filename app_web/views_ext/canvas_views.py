from .all_view_imports import *
from ..forms_ext.canvas_forms import *

def add_ops_transformation_canvas(request):
    if request.method == 'POST':
        form = OpsTransformationCanvasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ops_canvas_list')  # Redirect to the listing view
    else:
        form = OpsTransformationCanvasForm()
    return render(request, 'add_ops_canvas.html', {'form': form})


def list_ops_transformation_canvas(request):
    canvases = OpsTransformationCanvas.objects.all()
    return render(request, 'list_ops_canvases.html', {'canvases': canvases})


def update_ops_transformation_canvas(request, id):
    canvas = get_object_or_404(OpsTransformationCanvas, id=id)
    if request.method == 'POST':
        form = OpsTransformationCanvasForm(request.POST, instance=canvas)
        if form.is_valid():
            form.save()
            return redirect('ops_canvas_list')
    else:
        form = OpsTransformationCanvasForm(instance=canvas)
    return render(request, 'update_ops_canvas.html', {'form': form})


def delete_ops_transformation_canvas(request, id):
    canvas = get_object_or_404(OpsTransformationCanvas, id=id)
    if request.method == 'POST':
        canvas.delete()
        return redirect('ops_canvas_list')
    return render(request, 'delete_ops_canvas.html', {'canvas': canvas})
