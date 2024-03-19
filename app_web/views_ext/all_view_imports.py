from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
import os
import platform
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from ..models import *
from ..forms import *
from django.http import HttpResponseForbidden
from functools import wraps
from django.db.models import *
from django.http import Http404
from django.utils.html import strip_tags
import json
from django.http import JsonResponse
# Create your views here.
app_name = "app_web"
