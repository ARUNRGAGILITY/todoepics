from django.urls import path

from . import views

urlpatterns = [
    # all users will come to this visitor page
    path('', views.visitor_page, name="visitor_page"),
    # if login needed login page displayed
    path('login/', views.login_page, name="login"),
    # if registeration needed registration page displayed
    path('register/', views.register, name="register"),
    # user has logged in
    path('user-page/', views.user_page, name="user_page"),
    # logout page
    path('logout_page/', views.logout_page, name="logout_page"),
    # profile page
    path('profile_page/', views.profile_page, name="profile_page"),
]
