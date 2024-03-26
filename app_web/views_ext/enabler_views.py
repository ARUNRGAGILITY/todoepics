from .all_view_imports import *
from django.core.paginator import Paginator
from ..forms_ext.enabler_forms import *
app_name = 'app_web'

def ovs_types_list(request):
    ovs_types = OVS_Types.objects.filter(active=True)
    paginator = Paginator(ovs_types, 10)  # Show 10 items per page
    page = request.GET.get('page')
    ovs_types = paginator.get_page(page)
    context = {'ovs_types': ovs_types}
    template_file = f"{app_name}/_3admin/valuestream_mgmt/enablers/ovs_types_list.html"
    return render(request, template_file, context)

def ovs_types_create(request):
    if request.method == 'POST':
        # Handle form submission
        form = OVS_TypesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'OVS Type created successfully.')
            return redirect('ovs_types_list')
    else:
        # Display empty form
        form = OVS_TypesForm()
    context = {'form': form}
    template_file = f"{app_name}/_3admin/valuestream_mgmt/enablers/ovs_types_list.html"
    return render(request, template_file, context)

def ovs_types_edit(request, pk):
    ovs_type = get_object_or_404(OVS_Types, pk=pk)
    if request.method == 'POST':
        # Handle form submission
        form = OVS_TypesForm(request.POST, instance=ovs_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'OVS Type updated successfully.')
            return redirect('ovs_types_list')
    else:
        # Display form with existing data
        form = OVS_TypesForm(instance=ovs_type)
    context = {'form': form}
    template_file = f"{app_name}/_3admin/valuestream_mgmt/enablers/ovs_types_edit.html"
    return render(request, template_file, context)

def ovs_types_delete(request, pk):
    ovs_type = get_object_or_404(OVS_Types, pk=pk)
    if request.method == 'POST':
        ovs_type.delete()
        messages.success(request, 'OVS Type deleted successfully.')
        return redirect('ovs_types_list')
    context = {'ovs_type': ovs_type}
    template_file = f"{app_name}/_3admin/valuestream_mgmt/enablers/ovs_types_delete.html"
    return render(request, template_file, context)

def ovs_types_view(request, pk):
    ovs_type = get_object_or_404(OVS_Types, pk=pk)
    context = {'ovs_type': ovs_type}
    template_file = f"{app_name}/_3admin/valuestream_mgmt/enablers/ovs_types_view.html"
    return render(request, template_file, context)

def ovs_types_search(request):
    query = request.GET.get('q')
    ovs_types = OVS_Types.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    paginator = Paginator(ovs_types, 10)  # Show 10 items per page
    page = request.GET.get('page')
    ovs_types = paginator.get_page(page)
    context = {'ovs_types': ovs_types, 'query': query}
    template_file = f"{app_name}/_3admin/valuestream_mgmt/enablers/ovs_types_search.html"
    return render(request, template_file, context)
