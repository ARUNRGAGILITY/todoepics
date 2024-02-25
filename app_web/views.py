from django.shortcuts import render
import os
import platform
# Create your views here.
app_name = "app_web"

def home_page(request):
    # take inputs
    # process inputs
    
    # send outputs (info, template, request)
    context = {
        'page': 'home',
    }
    template_file = f"{app_name}/app_web_home.html"
    return render(request, template_file, context)
