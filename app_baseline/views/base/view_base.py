# all imports
from ..all_view_imports import *

# config
from ..._common.config.config import *
app_base_ref = base_app_ref
def landing_page(request):

    context = {'page': 'home', 'active_tag': 'home'}
    template_url = f"{app_base_ref}/base/visitor_page.html"
    return render(request, template_url, context)