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
from app_xpresskanban.models import *

def access_board(request, board_id):
    board = get_object_or_404(Board, board_id)
    RecentlyAccessedBoard.objects.create(user=request.user, board=board)

def user_dashboard(request):
    recently_accessed_boards = RecentlyAccessedBoard.objects.filter(user=request.user).order_by('-accessed_at')
    user_associated_boards = request.user.associated_boards.all()
    context = {
        'recently_accessed_boards': recently_accessed_boards,
        'user_associated_boards': user_associated_boards,
    }
    return render(request, 'user_dashboard.html', context)
