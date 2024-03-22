from django.http import HttpResponseForbidden
from ...models.list.model_list import *
from ...models.core_db.model_coredb import *
from ...models.permission.model_permission import *


def check_generic_permission(required_permission):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            model = kwargs.get('model')
            object_id = kwargs.get('object_id')

            content_type = ContentType.objects.get_for_model(model)
            
            try:
                obj = model.objects.get(id=object_id)
            except model.DoesNotExist:
                return HttpResponseForbidden('Object does not exist')

            # If the user who created the object is making the request, grant permission
            if obj.user == request.user:
                return view_func(request, *args, **kwargs)

            # Check individual permissions
            has_permission = GenericPermission.objects.filter(
                content_type=content_type,
                object_id=object_id,
                user=request.user,
                permission=required_permission
            ).exists()

            if has_permission:
                return view_func(request, *args, **kwargs)

            # Check group permissions
            user_groups = Group.objects.filter(user=request.user)

            has_group_permission = GenericPermission.objects.filter(
                content_type=content_type,
                object_id=object_id,
                group__in=user_groups,
                permission=required_permission
            ).exists()

            if has_group_permission:
                return view_func(request, *args, **kwargs)

            return HttpResponseForbidden('You do not have permission to view this page')
        
        return _wrapped_view
    return decorator
