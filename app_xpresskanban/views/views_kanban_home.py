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
import datetime

def learn_kanban(request):
    md_var = '''
# Learn Kanban
We will learn about Kanban in about 2mins...
## What is Kanban?
Kanban is a visual sign card or visual board in Japanese and Chinese version of the word Kanban.
Kanban is considered as two part word, Visual and Sign card.
## Why Kanban?
Kanban is utilized to signal to do some work or as per the context to make sure we have the permission
to do the work as per capacity and context.
## How to utilize Kanban?
Kanban can be utilized in a physical token format or in software like virtual token.
### Physical token approach
Physical token approach is considered to be strict in implementing the work-in-progress, because
once the token is available in the circulation or in the 'Kanban System' then only the work can be started.
### Virtual or software token approach
In the software driven approaches, where people utilize sticky-notes or post-it notes can utilize
a whiteboard and columns with WIP limits to indicate the capacity and limit the work-in-progress.
'''
    context = {'md_var':md_var}
    return render(request, 'app_xpresskanban/kanban_home_pages/learn_kanban.html', context)

def implement_kanban(request):
    md_var = '''
# Implement Kanban
We can implement Kanban using simple Physical boards and cards with Kanban's practices.
Since we are all working remotely or in hybrid mode, it is good to have online tools that can be
much easier to manage the work flow and cards, visually.
# How to decide which is better Online or Offline?
There are many considerations, here are few simple tips
- Team Locations
- Team's and Project Stakeholders location
- Ease of use
- Risks of losing post-it in office 
- Quick reference
## What is XpressKanban?
Xpress Kanban is one of the Kanban online tool implementation and it is an open-source software that provides the following...
- Simple to use interface
- Customizable
- Simple click option to move cards
- Simple spreadsheet type of option to edit cards and save information
- Edit columns / workflow, apply WIP Limits, Buffer columns, Swimlanes
- Follows Kanban practices
'''
    context = {'md_var':md_var}
    return render(request, 'app_xpresskanban/kanban_home_pages/implement_kanban.html', context)

def teach_kanban(request):
    md_var = '''
# Teach Kanban
Teaching Kanban practices and Kanban implementation can help you strengthen your understanding and also
share the knowledge that you have got in your implementation.
## How to start Teaching?
You can setup a local or office level Kanban Learning and Implementing community and start from there.

'''
    context = {'md_var':md_var}
    return render(request, 'app_xpresskanban/kanban_home_pages/teach_kanban.html', context)