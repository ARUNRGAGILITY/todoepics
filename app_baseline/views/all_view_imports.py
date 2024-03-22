# Imports for views
# Create your views here.
import os
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse, HttpResponseRedirect
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
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.core.serializers import serialize
from django.template import TemplateDoesNotExist, loader
from django.db import transaction
from django.http import QueryDict

from ..models.delivery.model_coredelivery import *
from ..models.delivery.model_delivery import *
from ..models.delivery.model_typeprioritystate import *

import logging


def get_model_class(value_type):
    model_classes = {
        # Delivery Type
        'Project': Project,
        'Product': Product,
        'Service': Service,
        'Solution': Solution,
        'ValueStream': ValueStream,
        'Organization': Organization,
        'Team': Team,
        'Members': Members,
        'Location': Location,
        
        # Delivery List of Values
        'BaseState': BaseState,
        'BasePriority': BasePriority,
        'BaseType': BaseType,
        # Add more mappings if needed
    }
    return model_classes.get(value_type)


