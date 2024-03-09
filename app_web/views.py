from django.shortcuts import render, redirect, HttpResponse
import os
import platform
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Create your views here.
app_name = "app_web"

def visitor_page(request):
    # take inputs
    # process inputs
    user = None
    which_template =  f"{app_name}/app_web_home.html"
    if request.method == 'POST': 
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print(f">>> === form valid === <<<")
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'user_page') # Provide a default redirect URL
            return redirect(next_url)
        else:
            print(f">>> === form invalid {form.errors} === <<<")
            # If you want to display form errors, ensure your template can display them
            messages.error(request, 'Username or password is incorrect')
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
    if request.method == 'POST': 
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print(f">>> === form valid === <<<")
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'user_page') # Provide a default redirect URL
            return redirect(next_url)
        else:
            print(f">>> === form invalid {form.errors} === <<<")
            # If you want to display form errors, ensure your template can display them
            messages.error(request, 'Username or password is incorrect')
    # send outputs (info, template, request)
    context = {
        'page': 'login',
    }
    template_file = f"{app_name}/_2user/login.html"
    return render(request, template_file, context)

# Registration Page
def register(request):
    # take inputs
    CORRECT_REG_CODE = "1"
    # process inputs
    if request.method == 'POST':
        # Retrieve the registration code from the form
        reg_code = request.POST.get('reg_code', '')
        
        # Check if the reg_code is alphanumeric and matches the correct registration code
        if not reg_code.isalnum() or reg_code != CORRECT_REG_CODE:
            messages.error(request, "Invalid or incorrect registration code.")
            # Return to the registration page with the form and error message
            return redirect("register")
        
        # Proceed with the standard registration process if the reg_code is valid
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to a success page after registration
            return redirect('user_page')
        else:
            # If the form is not valid, show form error messages
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")



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