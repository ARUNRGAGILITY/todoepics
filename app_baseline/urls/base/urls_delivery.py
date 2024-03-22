# Base URL configuration for app_abc
from django.urls import path, include


# base view
from ...views.base import view_base
from ...views.user import view_user
from ...views.list import view_list 
from ...views.type import view_type
from ...views.delivery import view_delivery
# config
from ..._common.config.config import *
app_base_ref = f"{base_app_ref}"

urlpatterns_delivery = [
    # delivery
    path('delivery_home', view_delivery.delivery_home ,name="delivery_home"),
]