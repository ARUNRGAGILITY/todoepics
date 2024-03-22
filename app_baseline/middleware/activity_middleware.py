from ..models.admin.model_useranalytics import *
# config
from .._common.config.config import *
# which app is being referred
app_base_ref = base_app_ref

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            # Log user activity here. Save the user and the visited page info.
            logger.debug(f">>> === User: {request.user.username} visited {request.path} === <<<")
            uam = UserVisited.objects.create(title="UA", user=request.user, path_visited=request.path)