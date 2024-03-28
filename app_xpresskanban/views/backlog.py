# Create your views here.
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mptt.exceptions import InvalidMove
from copy import copy
from copy import deepcopy
from mptt.exceptions import InvalidMove
from mptt.utils import tree_item_iterator
from mptt.templatetags.mptt_tags import cache_tree_children
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User, Group
import ast
import csv
from django.db.models import Q
from ..forms import *
# declare the different types of dynamic CRUD
def get_model_class(value_type):
    model_classes = {
        'Project': Project,
        'Product': Product,
        'Service': Service,
        'Solution': Solution,
        'ValueStream': ValueStream,
        # Add more mappings if needed
    }
    return model_classes.get(value_type)

@login_required(login_url='login')
def backlog_home(request, value_type, pk):
    model_name = value_type
    model_class = get_model_class(model_name)
    if model_class is not None:
        obj = get_object_or_404(model_class, pk=pk)
        context = {model_name: obj, 'object': obj, 'value_type': value_type}
        return render(request, 'app_xpresskanban/backlog_home.html', context)