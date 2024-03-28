from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import *

################################################################################
def get_model_class(value_type):
    model_classes = {
        'Project': Project,
        'Product': Product,
        'Service': Service,
        'Solution': Solution,
        'ValueStream': ValueStream,
        'Organization': Organization,
        'Team': Team,
        # Add more mappings if needed
    }
    return model_classes.get(value_type)


#
#
# TRYING THE GENERIC DECORATOR FOR SITE LEVEL / CERTAIN ADMIN 
#
#

from django.http import HttpResponseForbidden

def check_site_permissions_type(group_name,permission_denied_template='error_templates/site_permission_denied.html'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            # Check if the user is an admin or superuser
            if user.is_superuser or user.is_staff:
                return view_func(request, *args, **kwargs)
            
            # Check other users
            if user.is_authenticated and user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                 # Redirect to the custom permission-denied page
                response = render(request, permission_denied_template)
                response.status_code = 403  # Set the HTTP status code to Forbidden
                return response

        return _wrapped_view

    return decorator

#
#
#
#
#
from django.http import HttpResponse
def user_in_group(group_names, permission_denied_template='error_templates/permission_denied.html'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            # Check if the user is an admin or superuser
            if user.is_superuser or user.is_staff:
                return view_func(request, *args, **kwargs)
            if user.is_authenticated and user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            else:
                # Redirect to the custom permission-denied page
                response = render(request, permission_denied_template)
                response.status_code = 403  # Set the HTTP status code to Forbidden
                return response
        return _wrapped_view
    return decorator

#
#
# Check Board permissions with group type like view, edit, admin
#
#
from django.http import HttpResponse

def check_value_permissions_type(group_type, permission_denied_template='error_templates/value_permission_denied.html'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, value_type, pk, *args, **kwargs):
            model_name = value_type
            model_class = get_model_class(model_name)
            item_class = Board
            obj = get_object_or_404(model_class, pk=pk)
            view_group = f"{value_type}_{pk}_view"
            edit_group = f"{value_type}_{pk}_edit"
            admin_group = f"{value_type}_{pk}_admin"
            matching_groups = []
            user = request.user

            # Exempt the Staff and Admin users to utilize the required elements
            if user.is_superuser or user.is_staff:
                return view_func(request, value_type, pk, *args, **kwargs)
            
            # check what the user got and codify, then see what is required

            # what user got
            user_got = 0
            if user.groups.filter(name=view_group).exists():
                user_got = 10
            elif user.groups.filter(name=edit_group).exists():
                user_got = 20
            elif user.groups.filter(name=admin_group).exists():
                user_got = 30
            # what is required
            user_req = 0
            if group_type == "view":
                user_req = 10
            elif group_type == "edit":
                user_req = 20
            elif group_type == "admin":
                user_req = 30
            print(f">>> === USER REQ {user_req} AND USER GOT {user_got} check === <<<")
            # Check the user as per the need of the element
            if ( user.is_authenticated and (user_req <= user_got) or (user.groups.filter(name=view_group).exists() and group_type.lower() == "view")):
                matching_groups.append(view_group)
                request.matching_groups = matching_groups
                return view_func(request,  value_type, pk, *args, **kwargs)
            elif ( user.is_authenticated and (user_req <= user_got) or (user.groups.filter(name=edit_group).exists() and group_type.lower() == "edit")):
                matching_groups.append(edit_group)
                request.matching_groups = matching_groups
                return view_func(request,  value_type, pk, *args, **kwargs)
            elif ( user.is_authenticated and (user_req <= user_got) or (user.groups.filter(name=admin_group).exists() and group_type.lower() == "admin")):
                matching_groups.append(admin_group)
                request.matching_groups = matching_groups
                return view_func(request,  value_type, pk, *args, **kwargs)
            else:
                # Redirect to the custom permission-denied page
                context = {'message' : f"Group Type: {group_type} permissions expected." }
                response = render(request, permission_denied_template, context)
                response.status_code = 403  # Set the HTTP status code to Forbidden
                return response
        return _wrapped_view
    return decorator
#
#
# Check Value permissions
#
#
from django.http import HttpResponse

def check_value_permissions(permission_denied_template='error_templates/value_permission_denied.html'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, value_type, pk, *args, **kwargs):
            model_name = value_type
            model_class = get_model_class(model_name)
            item_class = Board
            obj = get_object_or_404(model_class, pk=pk)
            view_group = f"{value_type}_{pk}_view"
            edit_group = f"{value_type}_{pk}_edit"
            admin_group = f"{value_type}_{pk}_admin"
            matching_groups = []
            user = request.user
            if user.is_superuser or user.is_staff:
                return view_func(request, value_type, pk, *args, **kwargs)
            
            if user.is_authenticated and  user.groups.filter(name=view_group).exists():
                matching_groups.append(view_group)
                request.matching_groups = matching_groups
                return view_func(request,  value_type, pk, *args, **kwargs)
            elif user.is_authenticated and  user.groups.filter(name=edit_group).exists():
                matching_groups.append(edit_group)
                request.matching_groups = matching_groups
                return view_func(request,  value_type, pk, *args, **kwargs)
            elif user.is_authenticated and  user.groups.filter(name=admin_group).exists():
                matching_groups.append(admin_group)
                request.matching_groups = matching_groups
                return view_func(request,  value_type, pk, *args, **kwargs)
            else:
                # Redirect to the custom permission-denied page
                response = render(request, permission_denied_template)
                response.status_code = 403  # Set the HTTP status code to Forbidden
                return response
        return _wrapped_view
    return decorator


#
#
# Check Board permissions
#
#
from django.http import HttpResponse

def check_board_permissions(permission_denied_template='error_templates/board_permission_denied.html'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, value_type, pk, board_id, *args, **kwargs):
            model_name = value_type
            model_class = get_model_class(model_name)
            item_class = Board
            obj = get_object_or_404(model_class, pk=pk)
            item = get_object_or_404(item_class, id=board_id)
            view_group = f"Board_{board_id}_{value_type}_{pk}_view"
            edit_group = f"Board_{board_id}_{value_type}_{pk}_edit"
            admin_group = f"Board_{board_id}_{value_type}_{pk}_admin"
            matching_groups = []
            user = request.user
            if user.is_superuser or user.is_staff:
                return view_func(request, value_type, pk, board_id, *args, **kwargs)
            
            if user.is_authenticated and  user.groups.filter(name=view_group).exists():
                matching_groups.append(view_group)
                request.matching_groups = matching_groups
                return view_func(request,  value_type, pk, board_id,*args, **kwargs)
            elif user.is_authenticated and  user.groups.filter(name=edit_group).exists():
                matching_groups.append(edit_group)
                request.matching_groups = matching_groups
                return view_func(request,  value_type, pk, board_id,*args, **kwargs)
            elif user.is_authenticated and  user.groups.filter(name=admin_group).exists():
                matching_groups.append(admin_group)
                request.matching_groups = matching_groups
                return view_func(request,  value_type, pk, board_id,  *args, **kwargs)
            else:
                # Redirect to the custom permission-denied page
                response = render(request, permission_denied_template)
                response.status_code = 403  # Set the HTTP status code to Forbidden
                return response
        return _wrapped_view
    return decorator

#
#
# Check Board permissions with group type like view, edit, admin
#
#
from django.http import HttpResponse

def check_board_permissions_type(group_type, permission_denied_template='error_templates/board_permission_denied.html'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, value_type, pk, board_id, *args, **kwargs):
            model_name = value_type
            model_class = get_model_class(model_name)
            item_class = Board
            obj = get_object_or_404(model_class, pk=pk)
            item = get_object_or_404(item_class, id=board_id)
            view_group = f"Board_{board_id}_{value_type}_{pk}_view"
            edit_group = f"Board_{board_id}_{value_type}_{pk}_edit"
            admin_group = f"Board_{board_id}_{value_type}_{pk}_admin"
            matching_groups = []
            user = request.user

            # Exempt the Staff and Admin users to utilize the required elements
            if user.is_superuser or user.is_staff:
                return view_func(request, value_type, pk, board_id, *args, **kwargs)
            
            # check what the user got and codify, then see what is required

            # what user got
            user_got = 0
            if user.groups.filter(name=view_group).exists():
                user_got = 10
            elif user.groups.filter(name=edit_group).exists():
                user_got = 20
            elif user.groups.filter(name=admin_group).exists():
                user_got = 30
            # what is required
            user_req = 0
            if group_type == "view":
                user_req = 10
            elif group_type == "edit":
                user_req = 20
            elif group_type == "admin":
                user_req = 30
            print(f">>> === USER REQ {user_req} AND USER GOT {user_got} check === <<<")
            # Check the user as per the need of the element
            if ( user.is_authenticated and (user_req <= user_got) or (user.groups.filter(name=view_group).exists() and group_type.lower() == "view")):
                matching_groups.append(view_group)
                request.matching_groups = matching_groups
                return view_func(request,  value_type, pk, board_id,*args, **kwargs)
            elif ( user.is_authenticated and (user_req <= user_got) or (user.groups.filter(name=edit_group).exists() and group_type.lower() == "edit")):
                matching_groups.append(edit_group)
                request.matching_groups = matching_groups
                return view_func(request,  value_type, pk, board_id,*args, **kwargs)
            elif ( user.is_authenticated and (user_req <= user_got) or (user.groups.filter(name=admin_group).exists() and group_type.lower() == "admin")):
                matching_groups.append(admin_group)
                request.matching_groups = matching_groups
                return view_func(request,  value_type, pk, board_id,  *args, **kwargs)
            else:
                # Redirect to the custom permission-denied page
                context = {'message' : f"Group Type: {group_type} permissions expected." }
                response = render(request, permission_denied_template, context)
                response.status_code = 403  # Set the HTTP status code to Forbidden
                return response
        return _wrapped_view
    return decorator

#

#
# and group_type.lower() == "view"
#
#
#
from django.http import HttpResponse

def check_user_permissions(permission_denied_template='error_templates/permission_denied.html'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, value_type, *args, **kwargs):
            model_name = value_type
            model_class = get_model_class(model_name)
            if request.user.is_authenticated and  request.user in model_class.viewers.all():
                return view_func(request, *args, **kwargs)
            else:
                # Redirect to the custom permission-denied page
                response = render(request, permission_denied_template)
                response.status_code = 403  # Set the HTTP status code to Forbidden
                return response
        return _wrapped_view
    return decorator





############################################################################################

############################################################################################