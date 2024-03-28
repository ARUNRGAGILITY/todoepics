from .common_import_for_views import *
# declare the different types of dynamic CRUD

@login_required(login_url='login')
def global_configure(request):
    context = {}
    return render(request, 'app_xpresskanban/mvp2_0/global/configure.html', context)

@login_required(login_url='login')
def global_measure_metrics(request):
    context = {}
    return render(request, 'app_xpresskanban/mvp2_0/global/measure_metrics.html', context)

@login_required(login_url='login')
def global_kanban_settings(request):
    context = {}
    return render(request, 'app_xpresskanban/mvp2_0/global/kanban_settings.html', context)

@login_required(login_url='login')
def global_user_settings(request):
    context = {}
    return render(request, 'app_xpresskanban/mvp2_0/global/user_settings.html', context)