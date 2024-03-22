# Base URL configuration for app_abc
from django.urls import path, include


# base view
from ...views.base import view_base
from ...views.user import view_user
# config
from ..._common.config.config import *

app_base_ref = f"{base_app_ref}"

urlpatterns_user = [
    # user login process
    path('login/', view_user.loginPage, name="login"),
    path('logout/', view_user.logoutPage, name="logout"),
    path('register/',view_user.registerPage, name="register"),
    path('profile/',view_user.profile, name="profile"),
    path('password_change/', view_user.CustomPasswordChangeView.as_view(), name='password_change'),
    path('user-home/', view_user.user_home, name="user-home"),

]
