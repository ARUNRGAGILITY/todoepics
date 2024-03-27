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
from django.utils.html import strip_tags
import json
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from app_baseline.models.list.model_list import *
from app_baseline.forms.list.form_list import *
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
        if user.is_authenticated and (user.is_superuser or user.is_staff or AWProfile.objects.filter(user=user, roles__name__in=role_names).exists()):
            return True
        return False
    return user_passes_test_with_403(in_roles)

########### PROFILE and GENERAL links #################
@login_required
def my_profile_page(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'parent_page': 'my_profile',
        'page': 'my_profile_page',
        'user': user,
    }       
    template_file = f"{app_name}/_2user/my_profile_page.html"
    return render(request, template_file, context)
@login_required
def my_settings_page(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'parent_page': 'my_profile',
        'page': 'my_settings_page',
        'user': user,
    }       
    template_file = f"{app_name}/_2user/my_settings_page.html"
    return render(request, template_file, context)

@login_required
def my_workspace_page(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'parent_page': 'my_workspace',
        'page': 'my_workspace_page',
        'user': user,
    }       
    template_file = f"{app_name}/_2user/my_workspace_page.html"
    return render(request, template_file, context)

@login_required
def my_kanban(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'parent_page': 'my_workspace',
        'page': 'my_kanban',
        'user': user,
    }       
    template_file = f"{app_name}/_2user_ws/my_kanban.html"
    return render(request, template_file, context)

@login_required
def my_todolist(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'parent_page': 'my_workspace',
        'page': 'my_todolist',
        'user': user,
    }       
    template_file = f"{app_name}/_2user_ws/my_todolist.html"
    return render(request, template_file, context)

@login_required
def my_checklist(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'parent_page': 'my_workspace',
        'page': 'my_checklist',
        'user': user,
    }       
    template_file = f"{app_name}/_2user_ws/my_checklist.html"
    return render(request, template_file, context)

@login_required
def my_projects(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'parent_page': 'my_workspace',
        'page': 'my_projects',
        'user': user,
    }       
    template_file = f"{app_name}/_2user_ws/my_projects.html"
    return render(request, template_file, context)

#################################################### >>> MY ROLES
@login_required
def my_roles_page(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    profile = AWProfile.objects.get(user=user, active=True)
    roles = profile.roles.filter(active=True)
    # send outputs (info, template, request)
    context = {
        'parent_page': 'my_roles_page',
        'page': 'my_roles_page',
        'user': user,
        'roles': roles,
    }       
    template_file = f"{app_name}/_2user_roles/my_roles_page.html"
    return render(request, template_file, context)

@login_required
def my_admin_roles(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    profile = AWProfile.objects.get(user=user, active=True)
    roles = profile.roles.filter(active=True)
    # send outputs (info, template, request)
    context = {
        'parent_page': 'my_admin_roles',
        'page': 'my_admin_roles',
        'user': user,
        'roles': roles,
    }       
    template_file = f"{app_name}/_2user_roles/my_admin_roles.html"
    return render(request, template_file, context)

@login_required
def my_project_roles(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'parent_page': 'my_project_roles',
        'page': 'my_project_roles',
        'user': user,
    }       
    template_file = f"{app_name}/_2user_roles/my_project_roles.html"
    return render(request, template_file, context)

############################################################## >> my organizations
# the my_organizations_page is a landing page for user role 
# this will all the organizations summary or two broader authorized /viewable organizations links
@login_required
def my_organizations_page(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'parent_page': 'my_organizations_page',
        'page': 'my_organizations_page',
        'user': user,
    }       
    template_file = f"{app_name}/_2user_org/my_organizations_page.html"
    return render(request, template_file, context)


def is_org_admin(user, organization):
    return OrgAdmins.objects.filter(user=user, organization=organization).exists()

@login_required
def my_organization_admin_page(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'parent_page': 'my_organization_admin_page',
        'page': 'my_organization_admin_page',
        'user': user,
    }       
    template_file = f"{app_name}/_2user_org/my_organizations_page.html"
    return render(request, template_file, context)

@login_required
def organization_big_picture(request, id):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    organization = get_object_or_404(Organization, pk=id)
    org_admin = is_org_admin(user, organization)
    # send outputs (info, template, request)
    context = {
        'parent_page': 'organization_big_picture',
        'page': 'organization_big_picture',
        'user': user,
        'organization': organization,
        'is_org_admin': org_admin,
    }       
    template_file = f"{app_name}/_org/organization/organization_big_picture.html"
    return render(request, template_file, context)

@login_required
def organization_ref_arch(request, id):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    organization = get_object_or_404(Organization, pk=id)
    org_admin = is_org_admin(user, organization)
    # send outputs (info, template, request)
    context = {
        'parent_page': 'organization_ref_arch',
        'page': 'organization_ref_arch',
        'user': user,
        'organization': organization,
        'is_org_admin': org_admin,
    }       
    template_file = f"{app_name}/_org/organization/organization_ref_arch.html"
    return render(request, template_file, context)

@login_required
def my_authorized_organizations(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    profile = AWProfile.objects.get(user=user, active=True)
    organizations = profile.organizations.filter(active=True)
     # Prepare a subquery to check if the user is an OrgAdmin for the organization
    org_admins_subquery = OrgAdmins.objects.filter(
        user=user,
        organization_id=OuterRef('pk'),  # Links to the outer query's organization PK
    )

    # Annotate each organization with whether the user is an OrgAdmin for it
    authorized_organizations = Organization.objects.filter(active=True).annotate(
        is_org_admin=Exists(org_admins_subquery)
    ).order_by('name')  # Adding order for consistent results
    # send outputs (info, template, request)
    context = {
        'parent_page': 'my_authorized_organizations',
        'page': 'my_authorized_organizations',
        'user': user,
        'authorized_organizations': authorized_organizations,
    }       
    template_file = f"{app_name}/_2user_org/my_authorized_organizations.html"
    return render(request, template_file, context)
@login_required
def my_viewable_organizations(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    viewable_organizations = Organization.objects.filter(active=True)
     # Prepare a subquery to check if the user is an OrgAdmin for the organization
    org_admins_subquery = OrgAdmins.objects.filter(
        user=user,
        organization_id=OuterRef('pk'),  # Links to the outer query's organization PK
    )

    # Annotate each organization with whether the user is an OrgAdmin for it
    viewable_organizations = Organization.objects.filter(active=True).annotate(
        is_org_admin=Exists(org_admins_subquery)
    ).order_by('name')  # Adding order for consistent results
    # send outputs (info, template, request)
    context = {
        'parent_page': 'my_viewable_organizations',
        'page': 'my_viewable_organizations',
        'user': user,
        'viewable_organizations': viewable_organizations,
    }       
    template_file = f"{app_name}/_2user_org/my_viewable_organizations.html"
    return render(request, template_file, context)


# SITE ADMIN
@login_required
def site_admin_home(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    organizations = Organization.objects.filter(active=True)
    for org in organizations:
        org.admins = OrgAdmins.objects.filter(organization=org, active=True).select_related('user')

    # send outputs (info, template, request)
    context = {
        'parent_page': 'site_admin_home',
        'page': 'site_admin_home',
        'user': user,
        'organizations': organizations,
    }       
    template_file = f"{app_name}/_2admin_roles/site_admin/site_admin_home.html"
    return render(request, template_file, context)
@login_required
def ajax_user_suggestions(request):
    query = request.GET.get('query', '')
    if query:
        users = User.objects.filter(Q(username__icontains=query) | Q(id__icontains=query)) 
        suggestions = list(users.values('id', 'username'))
    else:
        suggestions = []
    return JsonResponse(suggestions, safe=False)

@login_required
def ajax_add_org_admin(request):
    user_id = request.POST.get('user_id')
    organization_id = request.POST.get('organization_id')

    # Ensure the user and organization exist
    user = get_object_or_404(User, pk=user_id)
    organization = get_object_or_404(Organization, pk=organization_id, active=True )

    # Create the OrgAdmins association
    OrgAdmins.objects.create(user=user, organization=organization, active=True)

    # Query all admins for this organization
    org_admins = OrgAdmins.objects.filter(organization=organization, active=True).select_related('user')
    admins_list = [{'id': admin.user.id, 'username': admin.user.username, 'org_id': admin.organization.id} for admin in org_admins]

    return JsonResponse({'status': 'success', 'admins': admins_list})

@login_required
def ajax_delete_org_admin(request):
    org_id = request.POST.get('org_id')
    user_id = request.POST.get('user_id')
    
    # Perform deletion
    OrgAdmins.objects.filter(organization_id=org_id, user_id=user_id).update(active=False, deleted=True)
    
    return JsonResponse({'status': 'success'})



# SITE ADMIN
@login_required
def org_admin_home(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    organizations = Organization.objects.filter(active=True)
    for org in organizations:
        org.admins = ProjectAdmins.objects.filter(organization=org, active=True).select_related('user')

    # send outputs (info, template, request)
    context = {
        'parent_page': 'site_admin_home',
        'page': 'site_admin_home',
        'user': user,
        'organizations': organizations,
    }       
    template_file = f"{app_name}/_2admin_roles/org_admin/org_admin_home.html"
    return render(request, template_file, context)


@login_required
def ajax_add_project_admin(request):
    user_id = request.POST.get('user_id')
    organization_id = request.POST.get('organization_id')

    # Ensure the user and organization exist
    user = get_object_or_404(User, pk=user_id)
    organization = get_object_or_404(Organization, pk=organization_id, active=True )

    # Create the OrgAdmins association
    ProjectAdmins.objects.create(user=user, organization=organization, active=True)

    # Query all admins for this organization
    project_admins = ProjectAdmins.objects.filter(organization=organization, active=True).select_related('user')
    admins_list = [{'id': admin.user.id, 'username': admin.user.username, 'org_id': admin.organization.id} for admin in project_admins]

    return JsonResponse({'status': 'success', 'admins': admins_list})

@login_required
def ajax_delete_project_admin(request):
    org_id = request.POST.get('org_id')
    user_id = request.POST.get('user_id')
    
    # Perform deletion
    ProjectAdmins.objects.filter(organization_id=org_id, user_id=user_id).update(active=False, deleted=True)
    
    return JsonResponse({'status': 'success'})

@login_required
def add_organization(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    form = OrganizationForm()
    
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the main page
            return redirect('site_admin_home')
        else:
            print(f">>> === form invalid {form.errors} === <<<")
    # send outputs (info, template, request)
    context = {
        'parent_page': 'site_admin_home',
        'page': 'add_organization',
        'user': user,
        'form': form,
    }       
    template_file = f"{app_name}/_2admin_roles/site_admin/add_organization.html"
    return render(request, template_file, context)

@login_required
def edit_organization(request, id):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    organization = get_object_or_404(Organization, pk=id)
    form = OrganizationForm(instance=organization)
    
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            # Redirect to the main page
            return redirect('site_admin_home')
        else:
            print(f">>> === form invalid {form.errors} === <<<")
    # send outputs (info, template, request)
    context = {
        'parent_page': 'site_admin_home',
        'page': 'edit_organization',
        'user': user,
        'form': form,
        'organization': organization,
    }       
    template_file = f"{app_name}/_2admin_roles/site_admin/edit_organization.html"
    return render(request, template_file, context)

@login_required
def delete_organization(request, id):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    organization = get_object_or_404(Organization, pk=id)
    organization.active = False
    organization.deleted = True
    organization.save()
    # Redirect to the main page
    return redirect('site_admin_home')

@login_required
def view_organization(request, id):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    organization = get_object_or_404(Organization, pk=id)
    # send outputs (info, template, request)
    context = {
        'parent_page': 'site_admin_home',
        'page': 'view_organization',
        'user': user,
        'organization': organization,
    }       
    template_file = f"{app_name}/_2admin_roles/site_admin/view_organization.html"
    return render(request, template_file, context)
    
    
# organization pages
# this is actual organization page,

@login_required
def organization_page(request, id):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    organization = get_object_or_404(Organization, pk=id)
    org_admin = is_org_admin(user, organization)
    # send outputs (info, template, request)
    context = {
        'parent_page': 'organization_page',
        'page': 'organization_page',
        'user': user,
        'organization': organization,
        'is_org_admin': org_admin,
    }       
    template_file = f"{app_name}/_org/organization/organization_page.html"
    return render(request, template_file, context)

# organization pages
@login_required
def organization_admin_page(request, id):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    organization = get_object_or_404(Organization, pk=id)
    org_admin = is_org_admin(user, organization)
    # send outputs (info, template, request)
    context = {
        'parent_page': 'organization_admin_page',
        'page': 'organization_admin_page',
        'user': user,
        'organization': organization,
        'is_org_admin': org_admin,
    }       
    template_file = f"{app_name}/_org/organization/organization_admin_page.html"
    return render(request, template_file, context)

def check_active_mapping_for_organization(organization_id):
    return MappingWBS.objects.filter(organization_id=organization_id, active=True).exists()
# organization pages
@login_required
def organization_wbs_page(request, id):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    organization = get_object_or_404(Organization, pk=id)
    org_admin = is_org_admin(user, organization)
    print(f">>> === org_admin {organization} === <<<")
    # step1: check the mappingwbs model to find out org id exists
    new_wbs = True
    if check_active_mapping_for_organization(organization.id):
        mapping_wbs = MappingWBS.objects.get(organization=organization, active=True)
        new_wbs = False               
    else:
        mapping_wbs = MappingWBS.objects.create(
                        name=f"{organization}-WBS", description="",
                        organization=organization, active=True)
        print(f">>> === Mapping does not exists **** created {mapping_wbs} === <<<")

    if new_wbs == False and  mapping_wbs.list is not None:
            print(f">>> === mapping exists === <<<")   
            print(f">>> === mapping exists go to regular page === <<<")
            return redirect('list_js_tree_id', list_id=mapping_wbs.list.id)
    # step2: create the entry for the list by round-trip 
    form = ListForm(request, type_type_filter='WorkBreakDownStructure')
    new_list = True 
    if request.method == 'POST':
        form = ListForm(request.user, type_type_filter='WorkBreakDownStructure', data=request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.parent = None
            new_list = False
            form.save()
            new_list_id = form.instance.id
            ref_type_id = form.instance.type
            mapping_wbs.list = form.instance
            mapping_wbs.save()
            print(f">>> === list form valid === <<<")
        else:
            print(f">>> === list form invalid {form} {form.errors} === <<<")
    # step3: create an entry for the type based on selection
    
    # if this is the first time, there is a round-trip for the wbs creation
   
    
    # send outputs (info, template, request)
    context = {
        'parent_page': 'organization_wbs_page',
        'page': 'organization_wbs_page',
        'user': user,
        'organization': organization,
        'is_org_admin': org_admin,
        'new_wbs': new_wbs,
        'new_list': new_list,
        'list': list,
        'mapping_wbs': mapping_wbs,
        'form': form,
    }       
    template_file = f"{app_name}/_org/organization/organization_wbs_page.html"
    return render(request, template_file, context)
############################################################ >> Starting links

def welcome(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'page': 'welcome',
        'user': user,
    }       
    template_file = f"{app_name}/welcome.html"
    return render(request, template_file, context)


def help(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'page': 'help',
        'user': user,
    }       
    template_file = f"{app_name}/_org/help.html"
    return render(request, template_file, context)
@login_required
def cafe(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'page': 'cafe',
        'user': user,
    }       
    template_file = f"{app_name}/_cafe/cafe.html"
    return render(request, template_file, context)
@login_required
def vsm(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'page': 'vsm',
        'user': user,
    }       
    template_file = f"{app_name}/_3admin/valuestream_mgmt/vsm.html"
    return render(request, template_file, context)

def about(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'page': 'about',
        'user': user,
    }       
    template_file = f"{app_name}/_org/about.html"
    return render(request, template_file, context)

def beaiagile(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'page': 'beaiagile',
        'user': user,
    }       
    template_file = f"{app_name}/_org/beaiagile.html"
    return render(request, template_file, context)

def organization_transformation(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'page': 'organization_transformation',
        'user': user,
    }       
    template_file = f"{app_name}/_org/organization_transformation.html"
    return render(request, template_file, context)

def transformation_leadership(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'page': 'transformation_leadership',
        'user': user,
    }       
    template_file = f"{app_name}/_org/transformation_leadership.html"
    return render(request, template_file, context)

def transformation_sw_training_services(request):
    # take inputs
    # process inputs
    user = None
    user = request.user   
    # send outputs (info, template, request)
    context = {
        'page': 'transformation_sw_training_services',
        'user': user,
    }       
    template_file = f"{app_name}/_org/transformation_sw_training_services.html"
    return render(request, template_file, context)

# this mostly not used / refactor
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
            print(f">>> === LOGIN PAGE === <<<")
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

# Registration Page (updated)
def register(request):
    # take inputs
    coding_ai = getattr(settings, 'CODING_AI', 'NOTHERE')
    print(f">>>=== CODINGAI: {coding_ai} === <<<")
    CORRECT_REG_CODE = coding_ai
    # process inputs
    if request.method == 'POST':
        # Retrieve the registration code from the form
        reg_code = request.POST.get('reg_code', '')
        
        # Check if the reg_code is alphanumeric and matches the correct registration code
        if CORRECT_REG_CODE != 'NOTHERE':
            if not reg_code.isalnum() or reg_code != CORRECT_REG_CODE:
                messages.error(request, f"Invalid or incorrect registration code.")
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
    user = request.user
    show_admin_link = user.is_superuser or user.is_staff or AWProfile.objects.filter(user=user, roles__name__in=["Admin", "SiteAdmin"]).exists()
    # send outputs (info, template, request)
    context = {
        'page': 'user_page',
        'show_admin_link': show_admin_link,
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
    user = request.user
    profile = AWProfile.objects.get(user=request.user)
    if user.is_superuser:
        form = SuperUserProfileForm(instance=profile)
    else:
        form = ProfileForm(instance=profile)
    if request.method == 'POST':
        if user.is_superuser:
            form = SuperUserProfileForm(request.POST, instance=profile)
        else:
            form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect to the profile page or wherever appropriate
            return redirect('profile_page')
    context = { 
               'parent_page': 'my_profile',
               'page': 'edit_profile',
                'form': form,
               }
    template_file = f"{app_name}/_2user/edit_profile.html"
    return render(request, template_file, context)


# Profile Page
@login_required
def profile_page(request):
     # take inputs
    # process inputs
    user = request.user
    profile, created = AWProfile.objects.get_or_create(user=request.user)
    show_admin_link = user.is_superuser or user.is_staff or AWProfile.objects.filter(user=user, roles__name__in=["Admin", "SiteAdmin"]).exists()
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
    profile, created = AWProfile.objects.get_or_create(user=request.user)
    show_admin_link = user.is_superuser or user.is_staff or AWProfile.objects.filter(user=user, roles__name__in=["Admin", "SiteAdmin"]).exists()
    # send outputs (info, template, request)
    context = {
        'page': 'profile_page',
        'user': user,
        'profile': profile,
        'show_admin_link': show_admin_link,
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
    profile, created = AWProfile.objects.get_or_create(user=request.user)
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
    profile, created = AWProfile.objects.get_or_create(user=request.user)
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
    profile, created = AWProfile.objects.get_or_create(user=request.user)
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
    profile, created = AWProfile.objects.get_or_create(user=request.user)
    parent = None
    objects = None
    objects_count = None
    steps = None
    ovs = None
    if vs == "ops":
        parent = OpsValueStream.objects.get(active=True, id=id)        
    elif vs == "dev":
        parent = DevValueStream.objects.get(active=True, id=id)
        ovs = parent.ops_valuestream
    else:
        print(f"Error No Ops/Dev VS identified")
    
    if parent:
        steps = parent.steps.all().filter(active=True)
        steps_details = [(step.id, step.name) for step in steps]  # Collecting step IDs and names
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
    context = {
        'page': 'dev_valuestream_mgmt',
        'user': user,
        'parent': parent,
        'object': parent, 
        'ovs': ovs,
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
    profile, created = AWProfile.objects.get_or_create(user=request.user)
    object = DevValueStream.objects.get(active=True, id=id)
    # processing
    form = DevValueStreamForm(instance=object)
    if request.method == 'POST':
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
    profile, created = AWProfile.objects.get_or_create(user=request.user)
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
    template_file = f"{app_name}/_3admin/valuestream_mgmt/edit_ops_valuestream.html"
    return render(request, template_file, context)



#####################################################
# ValueStream Mgmt main page
@login_required
def valuestream_mgmt(request):
    # take inputs
    # process inputs
    user = request.user
    profile, created = AWProfile.objects.get_or_create(user=request.user)   
    
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
def summary_ops_valuestream(request, id):
    # take inputs
    # process inputs
    steps_count = 0
    user = request.user
    profile, created = AWProfile.objects.get_or_create(user=request.user)   
    object = OpsValueStream.objects.get(active=True, id=id)
    dev_value_streams = DevValueStream.objects.filter(ops_valuestream=object).prefetch_related('supported_ops_steps')
    vsm_steps = ValueStreamSteps.objects.filter(active=True, opsvaluestream=object)
    ovs_dvs_count = object.devvaluestream.count()
    steps_count = vsm_steps.count()
    total_table_cols = (steps_count * 2) + 3
        
    steps_to_dev_streams = {}
    for dev_stream in DevValueStream.objects.all().prefetch_related('supported_ops_steps'):
        for step in dev_stream.supported_ops_steps.all():
            if step.id not in steps_to_dev_streams:
                steps_to_dev_streams[step.id] = [dev_stream.id]
            else:
                steps_to_dev_streams[step.id].append(dev_stream.id)
    # Your existing logic to fetch steps and other necessary data
    vsm_steps = ValueStreamSteps.objects.filter(opsvaluestream=object)  # Adjust as necessary
    # send outputs (info, template, request)
    context = {
        'page': 'ops_valuestream_mgmt',
        'user': user,
        'profile': profile,
        'object': object,
        'vs': 'ops',
        'vsm_steps': vsm_steps,
        'steps_count': steps_count,
        'total_table_cols': total_table_cols,
        'ops_value_stream': object,
        'dev_value_streams': dev_value_streams,
        'steps_to_dev_streams': steps_to_dev_streams,
        'ovs_dvs_count': ovs_dvs_count,
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/summary_ops_valuestream.html"
    return render(request, template_file, context)

#####################################################
# View Ops ValueStream 
@login_required
def view_ops_valuestream(request, id):
    # take inputs
    # process inputs
    steps_count = 0
    object = OpsValueStream.objects.get(active=True, id=id)    
    dev_valuestream_count = object.devvaluestream.filter(active=True).count()
    vsm_steps = ValueStreamSteps.objects.filter(active=True, opsvaluestream=object)
    steps_count = vsm_steps.count()
    # send outputs (info, template, request)
    context = {
        'page': 'ops_valuestream_mgmt',
        'object': object,
        'dev_valuestream_count': dev_valuestream_count,
        'vs': 'ops',
        'vsm_steps': vsm_steps,
        'steps_count': steps_count,   
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/view_ops_valuestream.html"
    return render(request, template_file, context)
#####################################################
# View Ops ValueStream 
@login_required
def view_dev_valuestream(request, id):
    # take inputs
    # process inputs
    user = request.user
    profile, created = AWProfile.objects.get_or_create(user=request.user)   
    object = DevValueStream.objects.get(active=True, id=id)
    parent = object.ops_valuestream.id
    vsm_steps = ValueStreamSteps.objects.filter(active=True, devvaluestream=object)
    # send outputs (info, template, request)
    steps_count = vsm_steps.count()
    total_table_cols = (steps_count * 2) + 3
    context = {
        'page': 'ops_valuestream_mgmt',
        'user': user,
        'profile': profile,
        'parent': parent,
        'object': object,
        'steps_count': steps_count,
        'total_table_cols': total_table_cols,
        'vs': 'dev',
        'id':id,
        'vsm_steps': vsm_steps,
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/view_dev_valuestream.html"
    return render(request, template_file, context)


#####################################################
# View Ops ValueStream 
@login_required
def summary_dev_valuestream(request, id):
    # take inputs
    # process inputs
    user = request.user
    profile, created = AWProfile.objects.get_or_create(user=request.user)   
    object = DevValueStream.objects.get(active=True, id=id)
    parent = object.ops_valuestream.id
    vsm_steps = ValueStreamSteps.objects.filter(active=True, devvaluestream=object)
    # send outputs (info, template, request)
    steps_count = vsm_steps.count()
    total_table_cols = (steps_count * 2) + 3
    context = {
        'page': 'summary_dev_valuestream',
        'user': user,
        'profile': profile,
        'parent': parent,
        'object': object,
        'steps_count': steps_count,
        'total_table_cols': total_table_cols,
        'vs': 'dev',
        'id':id,
        'vsm_steps': vsm_steps,
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/summary_dev_valuestream.html"
    return render(request, template_file, context)


#####################################################
# edit valuestream steps
@login_required
def edit_step(request, vs, ref_id, id):
    # take inputs
    # process inputs
    user = request.user
    profile, created = AWProfile.objects.get_or_create(user=request.user)
    object = ValueStreamSteps.objects.get(active=True, id=id)
    vsm_steps = None
    ovs = None
    dvs = None
    if vs == "ops":
        ovs = OpsValueStream.objects.get(active=True, id=ref_id)   
        vsm_steps = ValueStreamSteps.objects.filter(active=True, opsvaluestream=ovs)     
    elif vs == "dev":
        dvs = DevValueStream.objects.get(active=True, id=ref_id)
        ovs = dvs.ops_valuestream
        vsm_steps = ValueStreamSteps.objects.filter(active=True, devvaluestream=dvs)
    else:
        print(f"Error No Ops/Dev VS identified")
    steps_count = vsm_steps.count()
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
        'page': 'edit_step',
        'user': user,
        'profile': profile,
        'form': form,
        'vs': vs,
        'ref_id': ref_id,
        'id': id,
        'ovs': ovs,
        'dvs': dvs,
        'object': object,          
        'vsm_steps': vsm_steps,
        'steps_count': steps_count,       
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/edit_step.html"
    return render(request, template_file, context)

#####################################################
# edit valuestream steps
@login_required
def view_step(request, vs, ref_id, id):
    # take inputs
    # process inputs
    object = ValueStreamSteps.objects.get(active=True, id=id)
    # processing
    ovs = None
    dvs = None
    vsm_steps = None
    if vs == "ops":
        ovs = OpsValueStream.objects.get(active=True, id=ref_id)   
        vsm_steps = ValueStreamSteps.objects.filter(active=True, opsvaluestream=ovs)     
    elif vs == "dev":
        dvs = DevValueStream.objects.get(active=True, id=ref_id)
        ovs = dvs.ops_valuestream
        vsm_steps = ValueStreamSteps.objects.filter(active=True, devvaluestream=dvs)
    else:
        print(f"Error No Ops/Dev VS identified")
    
    steps_count = vsm_steps.count()
    
    # send outputs (info, template, request)
    context = {
        'page': 'view_step',
        'vs': vs,
        'ref_id': ref_id,
        'id': id,
        'ovs': ovs,
        'dvs': dvs,
        'object': object,   
        
        'vsm_steps': vsm_steps,
        'steps_count': steps_count,
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/view_step.html"
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
# def cafe_wbs(request):
#     themes = StrategicTheme.objects.prefetch_related(
#         'epics__features',
#         'epics__capabilities',
#         'epics__components',
#         'epics__features__user_stories',
#         'epics__features__spikes',
#         'epics__capabilities__user_stories',
#         'epics__capabilities__spikes',
#         'epics__features__user_stories__tasks',
#         'epics__features__spikes__tasks',
#         'epics__capabilities__spikes__tasks'
#     ).filter(active=True)
#     context = {'themes': themes, 'quarters': ['Q1', 'Q2', 'Q3', 'Q4']}
#     template_file = f"{app_name}/_cafe/mgmt/cafe_wbs.html"
#     return render(request, template_file, context)

# cafe_wbs
def build_hierarchy(start_nodes):
    """Build a nested dictionary representing the hierarchy starting from Strategic Themes."""
    hierarchy = {}
    
    for node in start_nodes:
        print(f">>> === >>>>>>>>>>>> {node} {node.title} {node.type.title}=== <<<")
        node_str = node.type.title.replace(" ", "")
        if node_str == 'StrategicTheme':
            hierarchy[node_str] = {'title': node.title, 'Epics': []}
            for child in node.get_children():
                print(f">>> === >>>>>>>>>>>> {child} {child.title} {child.type.title}=== <<<")
                if child.type.title == 'Epic':
                    epic_dict = {'title': child.title, 'Features': []}
                    for feature in child.get_children():
                        feature_dict = {'title': feature.title, 'UserStories': []}
                        for story in feature.get_children():
                            story_dict = {'title': story.title, 'Tasks': []}
                            for task in story.get_children():
                                task_dict = {'title': task.title}
                                story_dict['Tasks'].append(task_dict)
                            feature_dict['UserStories'].append(story_dict)
                        epic_dict['Features'].append(feature_dict)
                    hierarchy[node_str]['Epics'].append(epic_dict)
    
    return hierarchy

# In your view
def cafe_wbs(request):
    start_nodes = List.objects.filter(id=65, active=True)
    hierarchy = build_hierarchy(start_nodes)
    context = {'hierarchy': hierarchy}
    template_file = f"{app_name}/_cafe/mgmt/cafe_wbs.html"
    return render(request, template_file, context)



# delete ovs
@login_required(login_url='login')
def delete_ovs(request, id):
    object = get_object_or_404(OpsValueStream, id=id)
    context = {'object': object}
    if request.method == 'POST':
        OpsValueStream.objects.filter(id=id).update(active=False, deleted=False,  author=request.user)
        return redirect('ops_valuestream_mgmt')
    template_file = f"{app_name}/_3admin/valuestream_mgmt/delete_ops_valuestream.html"
    return render(request, template_file, context)

# add ovs 
@login_required(login_url='login')
def add_ovs(request):
    if request.method == 'POST':
        form = OpsValueStreamForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            vsm = form.save()            
            return redirect('ops_valuestream_mgmt')
    else:
        form = OpsValueStreamForm()
    
    context = {'page': 'add_ovs', 'form': form}
    template_file = f"{app_name}/_3admin/valuestream_mgmt/add_ops_valuestream.html"
    return render(request, template_file, context)
# add ovs 
@login_required(login_url='login')
def add_dvs(request, id):
    ovs = OpsValueStream.objects.get(active=True, id=id)       
    if request.method == 'POST':
        form = DevValueStreamForm(request.POST, initial={'ops_valuestream_id': ovs.id})
        if form.is_valid():
            form.instance.ops_valuestream = ovs
            form.instance.author = request.user
            vsm = form.save()            
            return redirect('dev_valuestream_mgmt', id=ovs.id)
    else:
        form = DevValueStreamForm(initial={'ops_valuestream_id': ovs.id})
    
    context = {'page': 'add_dvs', 'ovs': ovs, 'form': form}
    template_file = f"{app_name}/_3admin/valuestream_mgmt/add_dev_valuestream.html"
    return render(request, template_file, context)

@login_required(login_url='login')
def sorted_vsm_steps(request):
    if request.method == 'POST':
        ajax_data = request.POST['sorted_list_data']
        new_data = ajax_data.replace("[",'')
        new_data = new_data.replace("]",'')
        sorted_list = new_data.split(",")
        seq = 1
        for item in sorted_list:
            str = item.replace('"','')
            position = str.split('_')
            ValueStreamSteps.objects.filter(pk=position[0]).update(position=seq)
            seq = seq + 1
        context = {'ajax_data': ajax_data}
        template_file = f"{app_name}/_3admin/valuestream_mgmt/valuestream_steps.html"
        return render(request, template_file, context)


@login_required(login_url='login')
def ajaxupdate_valuestream_steps(request):
    if request.method == 'POST':
        print("AJAX CHECKBOX METHOD TEST")
        ajax_data = request.POST['checkbox_data']
        checkbox_details = ajax_data.split('_')
        checkbox_id = checkbox_details[0]
        checkbox_position = checkbox_details[1]
        checkbox_status = strip_tags(checkbox_details[2])
        obj = ValueStreamSteps.objects.filter(id=checkbox_id).update(title=checkbox_status)

        response_data = {}
        response_data['result'] = obj

        return JsonResponse(response_data)
    context = {'page': 'ajax_vssteps',}
    template_file = f"{app_name}/_3admin/valuestream_mgmt/valuestream_steps.html"
    return render(request, template_file, context)


# add vsm steps 
@login_required(login_url='login')
def add_vsm_steps(request, vs, id):
    if vs == "ops":
        parent = OpsValueStream.objects.get(active=True, id=id)        
    elif vs == "dev":
        parent = DevValueStream.objects.get(active=True, id=id)
    else:
        print(f"Error No Ops/Dev VS identified")
    print(f">>> === ADD VSM STEPS === <<<")
    if request.method == 'POST':
        form = ValueStreamStepsForm(request.POST)
        if form.is_valid():
            print(f">>> === form valid === <<<")
            if vs == "ops":
                form.instance.opsvaluestream = parent     
            elif vs == "dev":
                form.instance.devvaluestream = parent
            else:
                print(f"Error No Ops/Dev VS identified")
            form.instance.author = request.user
            vsm = form.save()            
            return redirect('valuestream_steps', vs=vs, id=id)
        else:
            print(f">>> === form invalid {form.errors} === <<<")
    else:
        form = ValueStreamStepsForm()
    
    context = {'page': 'add_vsm_steps', 
                'parent': parent,
                'vs': vs,
                'id': id,
               'form': form}
    template_file = f"{app_name}/_3admin/valuestream_mgmt/add_vsm_steps.html"
    return render(request, template_file, context)


# add vsm steps 
@login_required(login_url='login')
def delete_step(request, vs, ref_id, id):
    object = None
    parent = None
    if vs == "ops":
        parent = OpsValueStream.objects.get(active=True, id=ref_id)        
    elif vs == "dev":
        parent = DevValueStream.objects.get(active=True, id=ref_id)
    else:
        print(f"Error No Ops/Dev VS identified")
    object = get_object_or_404(ValueStreamSteps, id=id)
    context = {'object': object,
               'vs': vs,
               'ref_id': ref_id,
               'id':id,}
    if request.method == 'POST':
        if vs == "ops":
            parent = OpsValueStream.objects.get(active=True, id=ref_id)        
        elif vs == "dev":
            parent = DevValueStream.objects.get(active=True, id=ref_id)
        else:
            print(f"Error No Ops/Dev VS identified")
        ValueStreamSteps.objects.filter(id=id).update(active=False, deleted=True,  author=request.user)                
        return redirect('valuestream_steps', vs=vs, id=ref_id)
    template_file = f"{app_name}/_3admin/valuestream_mgmt/delete_step.html"
    return render(request, template_file, context)
        

## visually display the value stream step
## for ovs
#####################################################
# View Ops ValueStream 
@login_required(login_url='login')
def show_ovs_step_details(request, id):
    # take inputs
    # process inputs
    steps_count = 0
    object = OpsValueStream.objects.get(active=True, id=id)
    vsm_steps = ValueStreamSteps.objects.filter(active=True, opsvaluestream=object)
    steps_count = vsm_steps.count()
   
    # We are going to send the steps 4 columns per row
    # for displaying like post-it notes
    columns_per_row = 4
    rows = [vsm_steps[i:i + columns_per_row] for i in range(0, len(vsm_steps), columns_per_row)]


    # send outputs (info, template, request)
    context = {
        'page': 'ops_valuestream_mgmt', 
        'ovs': object,     
        'vsm_steps': vsm_steps,
        'steps_count': steps_count,
        'rows': rows,
        'vs': 'ops',
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/show_ovs_step_details.html"
    return render(request, template_file, context)
## visually display the value stream step
## for dvs
#####################################################
# View DVS ValueStream 
@login_required(login_url='login')
def show_dvs_step_details(request, ref_id, id):
    # take inputs
    # process inputs
    steps_count = 0
    ovs = None
    ovs = OpsValueStream.objects.get(active=True, id=ref_id)
    object = DevValueStream.objects.get(active=True, id=id)    
    vsm_steps = ValueStreamSteps.objects.filter(active=True, devvaluestream=object)
    steps_count = vsm_steps.count()
   
    # We are going to send the steps 4 columns per row
    # for displaying like post-it notes
    columns_per_row = 4
    rows = [vsm_steps[i:i + columns_per_row] for i in range(0, len(vsm_steps), columns_per_row)]


    # send outputs (info, template, request)
    context = {
        'page': 'ops_valuestream_mgmt', 
        'ovs': ovs,
        'dvs': object,     
        'vsm_steps': vsm_steps,
        'steps_count': steps_count,
        'rows': rows,
        'vs': 'dvs',
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/show_dvs_step_details.html"
    return render(request, template_file, context)

# 16032024
"""
  # Value stream canvas
    path('home_valuestream/', views.home_valuestream, name="home_valuestream"),
    
    # Value stream canvas
    path('home_devvaluestream_canvas/', views.home_devvaluestream_canvas, name="home_devvaluestream_canvas"),
    path('list_devvaluestream_canvas/', views.list_devvaluestream_canvas, name="list_devvaluestream_canvas"),
    # portfolio 
    path('home_portfolio_canvas/', views.home_portfolio_canvas, name="home_portfolio_canvas"),
    path('list_portfolio_canvas/', views.list_portfolio_canvas, name="list_portfolio_canvas"),
"""
## visually 
## for dvs
#####################################################
#  home portfolio canvas
@login_required(login_url='login')
def home_portfolio_canvas(request):
    # take inputs
    # process inputs
    
    # send outputs (info, template, request)
    context = {
        'page': 'home_portfolio_canvas',       
    }  
    template_file = f"{app_name}/_cafe/canvas/portfolio/home_portfolio_canvas.html"
    return render(request, template_file, context)
    
#####################################################
#  list  portfolio canvas
@login_required(login_url='login')
def list_portfolio_canvas(request):
    # take inputs
    # process inputs
    
    # send outputs (info, template, request)
    context = {
        'page': 'list_portfolio_canvas',       
    }  
    template_file = f"{app_name}/_cafe/canvas/portfolio/list_portfolio_canvas.html"
    return render(request, template_file, context)

#####################################################
#  list  portfolio canvas
@login_required(login_url='login')
def show_portfolio_canvas(request, id):
    # take inputs
    # process inputs
    
    # send outputs (info, template, request)
    context = {
        'page': 'show_portfolio_canvas',       
    }  
    template_file = f"{app_name}/_cafe/canvas/portfolio/show_portfolio_canvas.html"
    return render(request, template_file, context)
    
#####################################################
#  home devvaluestream canvas
@login_required(login_url='login')
def home_devvaluestream_canvas(request):
    # take inputs
    # process inputs
    
    # send outputs (info, template, request)
    context = {
        'page': 'home_devvaluestream_canvas',       
    }  
    template_file = f"{app_name}/_cafe/canvas/valuestream/home_devvaluestream_canvas.html"
    return render(request, template_file, context)

#####################################################
#  list devvaluestream canvas
@login_required(login_url='login')
def list_devvaluestream_canvas(request):
    # take inputs
    # process inputs
    
    # send outputs (info, template, request)
    context = {
        'page': 'list_devvaluestream_canvas',       
    }  
    template_file = f"{app_name}/_cafe/canvas/valuestream/list_devvaluestream_canvas.html"
    return render(request, template_file, context)



#####################################################
#   home_valuestream 
@login_required(login_url='login')
def home_valuestream(request):
    # take inputs
    # process inputs
    
    # send outputs (info, template, request)
    context = {
        'page': 'home_valuestream',       
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/home_valuestream.html"
    return render(request, template_file, context)

#####################################################
#   devops_ovs_transformation_canvas 
@login_required(login_url='login')
def devops_ovs_transformation_canvas(request, id):
    # take inputs
    # process inputs
    
    # send outputs (info, template, request)
    context = {
        'page': 'devops_ovs_transformation_canvas',       
    }  
    template_file = f"{app_name}/_3admin/valuestream_mgmt/devops_ovs_transformation_canvas.html"
    return render(request, template_file, context)

