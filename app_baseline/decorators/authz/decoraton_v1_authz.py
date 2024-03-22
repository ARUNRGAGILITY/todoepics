from ..all_decorators_imports import *


from ...models.list.model_list import * 
# Another decorator that sets permitted_nodes to None
def reset_permitted_nodes(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.permitted_nodes = None
        print(f">>> === **[[ PERMITTED NODES ]]** === <<<")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
# decorator
# @filter_list_tree_by_permission
def filter_list_tree_by_permission(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        print(f">>> === **[[ FILTER - PERMITTED NODES ]]** === <<<")
        permitted_nodes = List.objects.none()
        info_string = """
        For a given node_id, we are going to see if there is any users_can_view flag

        """
        print(f">>> === **** PERMITTED NODES {info_string} {permitted_nodes} **** === <<<")  

        # begin processing
        list_id = kwargs.get('list_id')
        nodes = List.objects.get(id=list_id)
        user = request.user
        print(f">>> === **** CRUCIAL {user} ===> {nodes} <<< **** === <<<")  

        # end processing

        request.permitted_nodes = permitted_nodes
        return view_func(request, *args, **kwargs)

    return _wrapped_view

