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
from django.db.models import Q, Count
from ..forms import *
# Create your views here.
# ops of the planner

# declare the different types of dynamic CRUD
def get_model_class(value_type):
    model_classes = {
        'Project': Project,
        'Product': Product,
        'Service': Service,
        'Solution': Solution,
        'ValueStream': ValueStream,
        'Organization': Organization,
        'Team': Team,
        # Add more mappings if needed
    }
    return model_classes.get(value_type)


######################################## Begin Board Settings ############################
# ops_project ==> ops_value
@login_required(login_url='login')
def board_settings(request, value_type, pk, board_id):
    model_name = value_type
    model_class = None
    item_count = 0
    model_class = get_model_class(model_name)
    item_class = Board
    obj = get_object_or_404(model_class, pk=pk)
    item = get_object_or_404(item_class, id=board_id)
    context = {'value_type': value_type,
                   'pk': pk, 'item_count': item_count,'item':item,
                   'object': obj, }
    return render(request, 'app_xpresskanban/board_settings/board_settings.html', context)