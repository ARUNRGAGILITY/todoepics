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
# Create your views here.
# ops of the planner
@login_required(login_url='login')
def kanban_home(request):
    context = {'page': 'Kanban', 'active_tab': 'kanban'}
    return render(request, 'app_xpresskanban/kanban_home.html', context)
@login_required(login_url='login')
def create_value(request, value_type):
    context = {'page': 'Create Value', 'active_tab': 'create_value',
               'value_type': value_type}
    return render(request, 'app_xpresskanban/create_value.html', context)



