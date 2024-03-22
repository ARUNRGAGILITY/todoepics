To achieve an "everyone can view" scenario, you can take several approaches. Here are a couple:

1. **Global Permission Flag**: Introduce a global flag in your `Permission` model to indicate if a permission is meant for "everyone". When this flag is set, all logged-in users can access the resource regardless of group membership.

   ```python
   class Permission(MPTTModel):
       # ...
       is_public = models.BooleanField(default=False)
       # ...
   ```

2. **Special 'Everyone' Group**: Create a special `CustomGroup` that all users are automatically a member of. Whenever a node is meant to be viewable by "everyone", this special group gets view permissions for that node.

### How to Implement

#### 1. Modify your Decorator

Modify the `filter_tree_by_permission` decorator to take this "everyone can view" scenario into account:

```python
from functools import wraps
from your_app.models import List, CustomGroup

def filter_tree_by_permission(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        node_id = kwargs.get('node_id')
        node = List.objects.get(id=node_id)
        permitted_nodes = List.objects.none()  # Start with an empty queryset

        for parent in node.get_ancestors(include_self=True):
            # Check if the node is marked as public
            if parent.permission.is_public:
                permitted_nodes = parent.get_descendants(include_self=True)
                break  # No need to check further
            
            custom_group = CustomGroup.objects.filter(users=request.user, permissions=parent.permission).first()
            if custom_group and custom_group.can_view:
                descendants = parent.get_descendants(include_self=True)
                permitted_nodes = permitted_nodes | descendants

        request.permitted_nodes = permitted_nodes
        return view_func(request, *args, **kwargs)

    return _wrapped_view
```

#### 2. Update Permission Creation Logic

When the admin creates the top-level nodes and sets them to be viewable by everyone, set the `is_public` flag to `True` for those nodes.

```python
def create_top_level_node(name):
    # Create the List and Permission instances as usual
    permission = Permission.objects.create(title=f"List_{name}_permission", is_public=True)
    List.objects.create(name=name, permission=permission)
```

Or, for the "Special 'Everyone' Group" approach:

```python
def create_top_level_node(name):
    # Create the List and Permission instances as usual
    permission = Permission.objects.create(title=f"List_{name}_permission")
    everyone_group = CustomGroup.objects.get(name="Everyone")
    everyone_group.permissions.add(permission)
    List.objects.create(name=name, permission=permission)
```

Either approach should make it easy to implement a scenario where "everyone" can view specific nodes.