# all imports
from ..all_view_imports import *
# specific imports
from ...forms.user.form_user import *
from ...forms.list.form_list import *
from ...models.user.model_user import *
from ...models.list.model_list import *

from ...decorators.authz.decorator_authorization import *

# config
from ..._common.config.config import *
# which app is being referred
app_base_ref = base_app_ref

@login_required(login_url='login')
def delivery_home(request):

    context = {'page': 'delivery'}
    template_url = f"{app_base_ref}/basics/delivery/delivery_home.html"
    return render(request, template_url, context)
