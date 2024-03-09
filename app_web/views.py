from django.shortcuts import render, redirect, HttpResponse
import os
import platform
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
app_name = "app_web"

def visitor_page(request):
    # take inputs
    # process inputs
    user = None
    which_template =  f"{app_name}/app_web_home.html"
    print(f">>> === >{request.user}< === <<<")
    if not request.user.is_authenticated:
        print(f">>> === {request.user} Not authenticated === <<<")
    else:
        print(f">>> === {request.user} check user === <<<")
        which_template = f"{app_name}/_2user/logged_in_user.html"
    
    if request.method == 'POST':        
        login_id = request.POST.get('login_id').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=login_id)
            user = authenticate(request, username=user.username, password=password)
            # process next url
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url != None:                
                    return redirect(next_url)
                return redirect('user_page')            
            else:
                messages.error(request, 'Username OR password does not exit')
        except:
            print(f">>>=== ERROR: LoginError: User {login_id} does not exist === <<<")
            messages.error(request, 'User does not exist 1')
       
    # send outputs (info, template, request)
    context = {
        'page': 'user_page',
        'user': user,
    }   
    
    template_file = which_template
    return render(request, template_file, context)

# Login Page
def login_page(request):
    # take inputs
    # process inputs
    
    # send outputs (info, template, request)
    context = {
        'page': 'login',
    }
    template_file = f"{app_name}/_2user/login.html"
    return render(request, template_file, context)

# Registration Page
def register(request):
    # take inputs
    # process inputs
    if request.method == 'POST':        
        login_id = request.POST.get('login_id').lower()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        reg_code = request.POST.get('reg_code')
        # Example reg_code validation
        expected_reg_code = "1"
        if reg_code != expected_reg_code:
            messages.error(request, 'Invalid registration code.')
            return redirect('register')
        if password1 and password1 == password2:
            # Check if user already exists
            if User.objects.filter(email=login_id).exists():
                messages.error(request, 'Email is already used.')
            else:
                # Assuming your User model has an email field or you're using a username that accepts emails
                user = User.objects.create_user(username=login_id, email=login_id, password=password1)
                user.save()
                print(f">>> === {user.username} === <<<")
                # Automatically log the user in after registration
                user = authenticate(request, username=login_id, password=password1)
                if user is not None:
                    login(request, user)
                    return redirect('user_page')
        else:
            messages.error(request, 'Passwords do not match.')


    # send outputs (info, template, request)
    context = {
        'page': 'register',
    }
    template_file = f"{app_name}/_2user/register.html"
    return render(request, template_file, context)

# User LoggedIn Page
def user_page(request):
    # take inputs
    # process inputs
    
    # send outputs (info, template, request)
    context = {
        'page': 'user_page',
    }
    template_file = f"{app_name}/_2user/logged_in_user.html"
    return render(request, template_file, context)

# Logout page
def logout_page(request):
    print(f">>> === {request.user} === <<<")
    logout(request)
    return redirect('/')