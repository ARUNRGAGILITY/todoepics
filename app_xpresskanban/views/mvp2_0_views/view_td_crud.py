from .common_import_for_views import *
# declare the different types of dynamic CRUD
def get_td_model_class(td_type):
    td_model_classes = {
       'Type': BaseType,
       'State': BaseState,
       'Priority': BasePriority,
    }
    return td_model_classes.get(td_type)
# TD CRUD
@login_required(login_url='login')
def list_td(request):
    context = {'page': 'List', 'active_tab': ''}
    return render(request,'app_xpresskanban/mvp2_0/td_crud/list_td.html', context)

@login_required(login_url='login')
def add_td(request):
    context = {'page': 'Add', 'active_tab': ''}
    return render(request,'app_xpresskanban/mvp2_0/td_crud/add_td.html', context)

@login_required(login_url='login')
def edit_td(request):
    context = {'page': 'Edit', 'active_tab': ''}
    return render(request,'app_xpresskanban/mvp2_0/td_crud/edit_td.html', context)

@login_required(login_url='login')
def view_td(request):
    context = {'page': 'View', 'active_tab': ''}
    return render(request,'app_xpresskanban/mvp2_0/td_crud/view_td.html', context)

@login_required(login_url='login')
def delete_td(request):
    context = {'page': 'Delete', 'active_tab': ''}
    return render(request,'app_xpresskanban/mvp2_0/td_crud/delete_td.html', context)

@login_required(login_url='login')
def copy_td(request):
    context = {'page': 'Copy', 'active_tab': ''}
    return render(request,'app_xpresskanban/mvp2_0/td_crud/copy_td.html', context)

@login_required(login_url='login')
def sorted_td(request):
    context = {'page': 'Sorted', 'active_tab': ''}
    return render(request,'app_xpresskanban/mvp2_0/td_crud/sorted_td.html', context)

@login_required(login_url='login')
def ops_td(request):
    context = {'page': 'Ops', 'active_tab': ''}
    return render(request,'app_xpresskanban/mvp2_0/td_crud/ops_td.html', context)

@login_required(login_url='login')
def show_deleted_td_items(request):
    context = {'page': 'Restore', 'active_tab': ''}
    return render(request,'app_xpresskanban/mvp2_0/td_crud/show_deleted_td_items.html', context)

@login_required(login_url='login')
def restore_bulk_deleted_td_items(request):
    context = {'page': 'Restore Bulk', 'active_tab': ''}
    return render(request,'app_xpresskanban/mvp2_0/td_crud/restore_bulk_deleted_td_items.html', context)

@login_required(login_url='login')
def restore_single_deleted_td_item(request):
    context = {'page': 'Restore Item', 'active_tab': ''}
    return render(request,'app_xpresskanban/mvp2_0/td_crud/restore_single_deleted_td_item.html', context)

