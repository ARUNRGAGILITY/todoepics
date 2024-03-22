from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from ...models.list.model_list import *

