# Base URL configuration for app_abc
from django.urls import path, include

# base view
from ...views.base import view_base
from ...views.user.view_user import *
# config
from ..._common.config.config import *
from .urls_user import urlpatterns_user
from .urls_group import urlpatterns_group
from .urls_list import urlpatterns_list
from .urls_type import urlpatterns_type
from .urls_delivery import urlpatterns_delivery
from .urls_permissions import urlpatterns_permission

urlpatterns_base = [
    # app URLS
    #path('', view_base.landing_page, name="landing_page"),    
] 

urlpatterns_base += urlpatterns_user
urlpatterns_base += urlpatterns_group
urlpatterns_base += urlpatterns_list
urlpatterns_base += urlpatterns_type
urlpatterns_base += urlpatterns_delivery
urlpatterns_base += urlpatterns_permission


