from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
import os
import platform
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from .forms import *
from django.http import HttpResponseForbidden
from functools import wraps
from django.db.models import *
from django.http import Http404
# Create your views here.
app_name = "app_web"

#######
def user_passes_test_with_403(test_func):
    """
    Decorator to make a view only confirm to a certain test,
    returning a 403 response if the test fails.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden('You do not have permission to view this page.')
        return _wrapped_view
    return decorator

def role_required(*role_names):
    """
    Requires user to be logged in and to have at least one of the specified roles.
    """
    def in_roles(user):
        if user.is_authenticated and (user.is_superuser or user.is_staff or Profile.objects.filter(user=user, roles__name__in=role_names).exists()):
            return True
        return False
    return user_passes_test_with_403(in_roles)


def visitor_page(request):
    # take inputs
    # process inputs
    user = None
    which_template =  f"{app_name}/app_web_home.html"
    user = request.user
    if request.method == 'POST': 
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print(f">>> === form valid === <<<")
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'user_page') # Provide a default redirect URL
            return redirect(next_url)
        else:
            print(f">>> === form invalid {form.errors} === <<<")
            # If you want to display form errors, ensure your template can display them
            messages.error(request, 'Username or password is incorrect')
    # send outputs (info, template, request)
    context = {
        'page': 'user_page',
        'user': user,
    }   
    
    template_file = which_template
    return render(request, template_file, context)

# Login Page
def login_page(request):
    # take inputs
    # process inputs
    if request.method == 'POST': 
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print(f">>> === form valid === <<<")
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'user_page') # Provide a default redirect URL
            return redirect(next_url)
        else:
            print(f">>> === form invalid {form.errors} === <<<")
            # If you want to display form errors, ensure your template can display them
            messages.error(request, 'Username or password is incorrect')
    # send outputs (info, template, request)
    context = {
        'page': 'login',
    }
    template_file = f"{app_name}/_2user/login.html"
    return render(request, template_file, context)

# Registration Page
def register(request):
    # take inputs
    CORRECT_REG_CODE = "1"
    # process inputs
    if request.method == 'POST':
        # Retrieve the registration code from the form
        reg_code = request.POST.get('reg_code', '')
        
        # Check if the reg_code is alphanumeric and matches the correct registration code
        if not reg_code.isalnum() or reg_code != CORRECT_REG_CODE:
            messages.error(request, "Invalid or incorrect registration code.")
            # Return to the registration page with the form and error message
            return redirect("register")
        
        # Proceed with the standard registration process if the reg_code is valid
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to a success page after registration
            return redirect('user_page')
        else:
            # If the form is not valid, show form error messages
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")



    # send outputs (info, template, request)
    context = {
        'page': 'register',
    }
    template_file = f"{app_name}/_2user/register.html"
    return render(request, template_file, context)

# User LoggedIn Page
@login_required
def user_page(request):
    # take inputs
    # process inputs
    
    # send outputs (info, template, request)
    context = {
        'page': 'user_page',
    }
    template_file = f"{app_name}/_2user/logged_in_user.html"
    return render(request, template_file, context)

# Logout page
def logout_page(request):
    print(f">>> === {request.user} === <<<")
    logout(request)
    return redirect('/')

# edit User profile
@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to the profile page or wherever appropriate
            return redirect('profile_page')

    template_file = f"{app_name}/_2user/edit_profile.html"
    return render(request, template_file, {'form': form})


# Profile Page
@login_required
def profile_page(request):
     # take inputs
    # process inputs
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)
    show_admin_link = user.is_superuser or user.is_staff or Profile.objects.filter(user=user, roles__name__in=["Admin", "SiteAdmin"]).exists()
    # send outputs (info, template, request)
    context = {
        'page': 'profile_page',
        'user': user,
        'profile': profile,
        'show_admin_link': show_admin_link,
    }  
    template_file = f"{app_name}/_2user/profile_page.html"
    return render(request, template_file, context)


## Admin Page ##
@role_required('SiteAdmin', 'Admin')  # Example roles
def admin_page(request):
    # take inputs
    # process inputs
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)

    # send outputs (info, template, request)
    context = {
        'page': 'profile_page',
        'user': user,
        'profile': profile,
    }  
    template_file = f"{app_name}/_3admin/admin_page.html"
    return render(request, template_file, context)

#####################################################
# Roles Mgmt
@login_required
def roles_mgmt(request):
    # take inputs
    # process inputs
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)
    objects = Role.objects.filter(active=True).order_by('position')
    objects_count = objects.count()
    # processing
    form = RoleForm()
    if request.method == 'POST':
        print(f">>> === post method === <<<")
        form = RoleForm(request.POST)
        if form.is_valid():
            print(f">>> === form valid === <<<")
            form.save()
            # Redirect to the main page
            return redirect('roles_mgmt')
        else:
            print(f">>> === form invalid {form.errors} === <<<")
        
    
    # send outputs (info, template, request)
    context = {
        'page': 'roles_mgmt',
        'user': user,
        'profile': profile,
        'objects': objects,
        'objects_count': objects_count,
    }  
    template_file = f"{app_name}/_3admin/roles_mgmt/roles_mgmt.html"
    return render(request, template_file, context)


#####################################################
# ValueStream Mgmt
@login_required
def ops_valuestream_mgmt(request):
    # take inputs
    # process inputs
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)
    # Get the ContentType for OpsValueStream
    
    objects = OpsValueStream.objects.filter(active=True).order_by('position').annotate(
        dev_valuestream_count=Count('devvaluestream', filter=Q(devvaluestream__active=True)),        
    )
    objects_count = objects.count()

    for ops_valuestream in objects:
        # Directly use the 'steps' related_name for filtering active steps
        steps_count = ops_valuestream.steps.filter(active=True).count()  
        print(f">>> === ********** {ops_valuestream} steps_count {steps_count} === <<<")      
        # Attach the count to each ops_valuestream object dynamically
        ops_valuestream.steps_count = steps_count
    # processing
    form = OpsValueStreamForm()
    if request.method == 'POST':
        print(f">>> === post method === <<<")
        form = OpsValueStreamForm(request.POST)
        if form.is_valid():
            print(f">>> === form valid === <<<")
            form.save()
            # Redirect to the main page
            return redirect('ops_valuestream_mgmt')
        else:
            print(f">>> === form invalid {form.errors} === <<<")
        
    
    # send outputs (info, template, request)
    context = {
        'page': 'ops_valuestream_mgmt',
        'user': user,
        'profile': profile,
        'objects': objects,
        'objects_count': objects_count,
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/ops_valuestream_mgmt.html"
    return render(request, template_file, context)


#####################################################
# ValueStream Mgmt
@login_required
def dev_valuestream_mgmt(request, id):
    # take inputs
    # process inputs
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)
    parent = OpsValueStream.objects.get(active=True, id=id)
    objects = DevValueStream.objects.filter(active=True, ops_valuestream=parent).order_by('position')
    objects_count = objects.count()    
    # processing
    form = DevValueStreamForm()
    if request.method == 'POST':
        print(f">>> === post method === <<<")
        form = DevValueStreamForm(request.POST)
        if form.is_valid():
            print(f">>> === form valid === <<<")
            dev_valuestream = form.save(commit=False)
            dev_valuestream.ops_valuestream = parent
            dev_valuestream.save()
            # Redirect to the main page
            return redirect('dev_valuestream_mgmt', id=id)
        else:
            print(f">>> === form invalid {form.errors} === <<<")
        
    
    # send outputs (info, template, request)
    context = {
        'page': 'dev_valuestream_mgmt',
        'user': user,
        'parent': parent,
        'profile': profile,
        'objects': objects,
        'objects_count': objects_count,
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/dev_valuestream_mgmt.html"
    return render(request, template_file, context)


#####################################################
# ValueStream Steps
@login_required
def valuestream_steps(request, vs, id):
    # take inputs
    # process inputs
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)
    parent = None
    objects = None
    objects_count = None
    steps = None
    if vs == "ops":
        parent = OpsValueStream.objects.get(active=True, id=id)        
    elif vs == "dev":
        parent = DevValueStream.objects.get(active=True, id=id)
    else:
        print(f"Error No Ops/Dev VS identified")
    
    print(f">>> === IDENTIFIED vs={vs},id={id},parent={parent},parent.id={parent.id} === <<<")
    if parent:
        print(f">>> === IDENTIFIED2: content_type:{parent} === <<<")
        steps = parent.steps.all()
        steps_details = [(step.id, step.name) for step in steps]  # Collecting step IDs and names
        print(f">>> === IDENTIFIED3: objects:{objects}, steps={steps} === <<<")
        objects_count = steps.count()   
    # processing
    form = ValueStreamStepsForm()
    if request.method == 'POST':
        print(f">>> === post method === <<<")
        form = ValueStreamStepsForm(request.POST)
        if form.is_valid():
            step = form.save(commit=False)
            if vs == 'ops':
                step.opsvaluestream = parent
            elif vs == 'dev':
                step.devvaluestream = parent
            step.save()
            # Redirect to the main page
            return redirect('valuestream_steps', vs=vs, id=id)
        else:
            print(f">>> === form invalid {form.errors} === <<<")
        
    
    # send outputs (info, template, request)
    print(f">>> === CHECKING----> VS={vs},id={id} === <<<")
    context = {
        'page': 'dev_valuestream_mgmt',
        'user': user,
        'parent': parent,
        'profile': profile,
        'objects': objects,
        'objects_count': objects_count,
        'steps_details': steps_details,
        'steps': steps,
        'vs': vs,
        'id': id,
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/valuestream_steps.html"
    return render(request, template_file, context)

#####################################################
# edit dev valuestream
@login_required
def edit_dev_valuestream(request, id):
    # take inputs
    # process inputs
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)
    object = DevValueStream.objects.get(active=True, id=id)
    print(f">>> === devvs {object} === <<<")
    # processing
    form = DevValueStreamForm(instance=object)
    if request.method == 'POST':
        print(f">>> === post method === <<<")
        form = DevValueStreamForm(request.POST, instance=object)
        if form.is_valid():
            print(f">>> === form valid === <<<")
            form.save()
            # Redirect to the main page
            return redirect('dev_valuestream_mgmt', id=object.ops_valuestream.id)
        else:
            print(f">>> === form invalid {form.errors} === <<<")
        
    
    # send outputs (info, template, request)
    context = {
        'page': 'edit_dev_valuestream',
        'user': user,
        'profile': profile,
        'object': object,
        'form': form,
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/edit_dev_valuestream.html"
    return render(request, template_file, context)

#####################################################
# edit ops valuestream
@login_required
def edit_ops_valuestream(request, id):
    # take inputs
    # process inputs
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)
    object = OpsValueStream.objects.get(active=True, id=id)
    print(f">>> === opsvs {object} === <<<")
    # processing
    form = OpsValueStreamForm(instance=object)
    if request.method == 'POST':
        print(f">>> === post method === <<<")
        form = OpsValueStreamForm(request.POST, instance=object)
        if form.is_valid():
            print(f">>> === form valid === <<<")
            form.save()
            # Redirect to the main page
            return redirect('ops_valuestream_mgmt')
        else:
            print(f">>> === form invalid {form.errors} === <<<")
        
    
    # send outputs (info, template, request)
    context = {
        'page': 'edit_dev_valuestream',
        'user': user,
        'profile': profile,
        'object': object,
        'form': form,
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/edit_dev_valuestream.html"
    return render(request, template_file, context)



#####################################################
# ValueStream Mgmt main page
@login_required
def valuestream_mgmt(request):
    # take inputs
    # process inputs
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)   
    
    # send outputs (info, template, request)
    context = {
        'page': 'ops_valuestream_mgmt',
        'user': user,
        'profile': profile,
       
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/valuestream_mgmt.html"
    return render(request, template_file, context)

#####################################################
# View Ops ValueStream 
@login_required
def view_ops_valuestream(request, id):
    # take inputs
    # process inputs
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)   
    object = OpsValueStream.objects.get(active=True, id=id)
    # send outputs (info, template, request)
    context = {
        'page': 'ops_valuestream_mgmt',
        'user': user,
        'profile': profile,
        'object': object,
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/view_ops_valuestream.html"
    return render(request, template_file, context)

#####################################################
# edit valuestream steps
@login_required
def edit_step(request, vs, ref_id, id):
    # take inputs
    # process inputs
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)
    object = ValueStreamSteps.objects.get(active=True, id=id)
    print(f">>> === opsvs {object} === <<<")
    # processing
    form = ValueStreamStepsForm(instance=object)
    if request.method == 'POST':
        print(f">>> === post method === <<<")
        form = ValueStreamStepsForm(request.POST, instance=object)
        if form.is_valid():
            print(f">>> === form valid === <<<")
            form.save()
            # Redirect to the main page
            return redirect('valuestream_steps', vs=vs, id=ref_id)
        else:
            print(f">>> === form invalid {form.errors} === <<<")
        
    
    # send outputs (info, template, request)
    context = {
        'page': 'edit_dev_valuestream',
        'user': user,
        'profile': profile,
        'object': object,
        'form': form,
       
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/edit_step.html"
    return render(request, template_file, context)


## CAFE
def cafe_start(request):
    themes = StrategicTheme.objects.prefetch_related('objectives__key_results__quarterly_measures').all()
    context = {'themes': themes, 'quarters': ['Q1', 'Q2', 'Q3', 'Q4']}
    template_file = f"{app_name}/_cafe/biz/strategic_theme.html"
    return render(request, template_file, context)

# list of all strategic themes
def index_st(request):
    themes = StrategicTheme.objects.filter(active=True).all()
    context = {'themes': themes, 'quarters': ['Q1', 'Q2', 'Q3', 'Q4']}
    template_file = f"{app_name}/_cafe/biz/index_st.html"
    return render(request, template_file, context)

# strategic theme detail
def st_detail(request, theme_id):
    theme = get_object_or_404(StrategicTheme, pk=theme_id, active=True)
    try:
        next_theme = theme.get_next_by_created_at(active=True)
    except StrategicTheme.DoesNotExist:
        next_theme = None

    try:
        prev_theme = theme.get_previous_by_created_at(active=True)
    except StrategicTheme.DoesNotExist:
        prev_theme = None

    context = {
        'theme': theme,
        'next_theme': next_theme,
        'prev_theme': prev_theme,
    }
    template_file = f"{app_name}/_cafe/biz/st_detail.html"
    return render(request, template_file, context)

# cafe_wbs
def cafe_wbs(request):
    themes = StrategicTheme.objects.prefetch_related(
        'epics__features',
        'epics__capabilities',
        'epics__features__user_stories',
        'epics__capabilities__spikes',
        'epics__features__user_stories__tasks',
        'epics__capabilities__spikes__tasks'
    ).filter(active=True)
    context = {'themes': themes, 'quarters': ['Q1', 'Q2', 'Q3', 'Q4']}
    template_file = f"{app_name}/_cafe/mgmt/cafe_wbs.html"
    return render(request, template_file, context)