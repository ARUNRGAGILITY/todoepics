```
from django.contrib.contenttypes.models import ContentType
from .models import GenericPermission, YourModel  # replace YourModel with the model you're using
from django.contrib.auth.models import User

# Get ContentType for the model
content_type = ContentType.objects.get_for_model(YourModel)

# Assume we're working with an object of YourModel with id=1
object_id = 1

# Assume we're setting permission for user with id=1
user = User.objects.get(id=1)

# Now create a GenericPermission entry
permission = GenericPermission.objects.create(
    content_type=content_type,
    object_id=object_id,
    user=user,
    permission=GenericPermission.VIEW  # Or EDIT/ADMIN
)

```