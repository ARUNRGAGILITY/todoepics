from datetime import timedelta
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
from datetime import date

# Create your views here.
# ops of the planner
from datetime import timedelta


# def calculate_cycle_time(cardmovement):
#     return cardmovement.moved_at - cardmovement.card.created_at

# def calculate_cycle_time_avg(cardmovements):
#     total_cycle_time = sum(calculate_cycle_time(movement).total_seconds() for movement in cardmovements)
#     return total_cycle_time / len(cardmovements) if cardmovements else 0

# def calculate_lead_time(cardmovement):
#     done_movement = cardmovement.card.cardmovement_set.filter(target_column__title='Done').first()
#     if done_movement:
#         return done_movement.moved_at - cardmovement.card.created_at
#     else:
#         return timedelta(seconds=0)  # Card hasn't been completed yet

# # Calculate average lead time
# def calculate_lead_time_avg(cardmovements):
#     total_lead_time = sum(calculate_lead_time(movement).total_seconds() for movement in cardmovements)
#     return total_lead_time / len(cardmovements) if cardmovements else 0

# # # calculating metrics
# # def calculate_cycle_time_avg(board, start_date, end_date):
# #     card_movements = CardMovement.objects.filter(card__board=board, 
# #                                                  moved_at__range=(start_date, end_date))
# #     print(f">>>> CARDMOVEMENTS: {board} ==> {start_date} ==> {end_date} ==> {card_movements}")
# #     total_cycle_time = sum((movement.moved_at - movement.card.created_at).total_seconds() for movement in card_movements)
# #     return total_cycle_time / len(card_movements) if card_movements else 0

# # try1
# # def calculate_lead_time_avg(board, start_date, end_date):
# #     completed_cards = CORE_HSDB.objects.filter(board=board, 
# #                                                cardmovement__target_column__title='Done', 
# #                                                cardmovement__moved_at__range=(start_date, 
# #                                                                               end_date))
# #     print(f">>>>> completed_cards {board} ==> {start_date} ==> {end_date} ==> {completed_cards}")
# #     total_lead_time = sum((card.cardmovement_set.filter(target_column__title='Done').first().moved_at - card.created_at).total_seconds() for card in completed_cards)
# #     return total_lead_time / len(completed_cards) if completed_cards else 0

# # try2
# # from django.db.models import ExpressionWrapper, F, DurationField, Sum
# # def calculate_lead_time_avg(board, start_date, end_date):
# #     completed_cards = CORE_HSDB.objects.filter(
# #         board=board,
# #         cardmovement__target_column__title='Done',
# #         cardmovement__moved_at__range=(start_date, end_date)
# #     ).annotate(
# #         lead_time=ExpressionWrapper(
# #             F('cardmovement__moved_at') - F('created_at'),
# #             output_field=DurationField()
# #         )
# #     ).exclude(lead_time=None)

# #     total_lead_time = completed_cards.aggregate(Sum('lead_time'))['lead_time__sum']
# #     completed_count = completed_cards.count()

# #     return total_lead_time / completed_count if completed_count > 0 else 0

# # Storing metrics

# def calculate_and_store_metrics(board):
#     today = date.today()
#     start_date = today - timedelta(days=30)  # Change as needed
#     end_date = today
#     cycle_time_avg = calculate_cycle_time_avg(board, start_date, end_date)
#     lead_time_avg = calculate_lead_time_avg(board, start_date, end_date)
    
#     Metrics.objects.create(board=board, date=today, cycle_time_avg=cycle_time_avg, lead_time_avg=lead_time_avg)

# # report generation
# def board_metrics(request, board_id):
#     board = Board.objects.get(pk=board_id)
#     calculate_and_store_metrics(board)  # Calculate and store metrics for today
#     metrics = Metrics.objects.filter(board=board)
#     context =  {'board': board, 'metrics': metrics}
#     return render(request, 'app_xpresskanban/metrics/board_metrics.html', context)

from datetime import date, timedelta

def calculate_cycle_time(cardmovement):
    ret_calc = cardmovement.moved_at - cardmovement.card.created_at
    print(f">>>>> CCT: {ret_calc}")
    return ret_calc
def calculate_lead_time(cardmovement):
    done_movement = cardmovement.card.cardmovement_set.filter(target_column__title='Done').first()
    if done_movement:
        return done_movement.moved_at - cardmovement.card.created_at
    else:
        return timedelta(seconds=0)  # Card hasn't been completed yet
def calculate_cycle_time_avg(cardmovements):
    total_cycle_time = sum(calculate_cycle_time(movement).total_seconds() for movement in cardmovements)
    t_cards = len(cardmovements)
    avg_ct = total_cycle_time / t_cards  if cardmovements else 0    
    avg_ct_hrs = round(avg_ct / 3600, 2)
    print(f"Total Cards: {t_cards, {cardmovements}}")
    print(f"AVG CT: {avg_ct} ==> {avg_ct_hrs}hrs")
    return avg_ct_hrs
from datetime import timedelta

def calculate_lead_time_avg(completed_cards):
    total_lead_time = timedelta(seconds=0)
    completed_card_count = len(completed_cards)
    for card in completed_cards:
        card_movement = CardMovement.objects.filter(card=card).first()
        if card_movement and card.created_at:
            lead_time = card_movement.moved_at - card.created_at
            total_lead_time += lead_time
    #return total_lead_time.total_seconds() / completed_card_count if completed_card_count else 0
    average_lead_time_seconds = total_lead_time.total_seconds() / completed_card_count if completed_card_count else 0
    average_lead_time_hours = round(average_lead_time_seconds / 3600, 2)  # Convert to hours and round off
    return average_lead_time_hours



def calculate_and_store_metrics(board):
    today = date.today()
    start_date = today - timedelta(days=30)  
    end_date = today

    # Get the completed cards
    completed_cards = CORE_HSDB.objects.filter(board=board,
                                               cardmovement__target_column__title='Done')
    print(f">>>>>> {completed_cards}")

    # all the board level cards
    board_cards = CORE_HSDB.objects.filter(board=board)
    card_movements = CardMovement.objects.filter(card__board=board)
    completed_cards = CORE_HSDB.objects.filter(board=board, 
                                               cardmovement__target_column__title='Done', 
                                               #cardmovement__moved_at__range=(start_date, end_date)
                                               )
    print(f">>> CARDMOVEMENTS 00000 CHECK {card_movements} ")
    cycle_time_avg = calculate_cycle_time_avg(card_movements)
    lead_time_avg = calculate_lead_time_avg(completed_cards)
    print(f">>>> GOT the CT and LT: {cycle_time_avg}/{lead_time_avg}")
    Metrics.objects.create(board=board, date=today, cycle_time_avg=cycle_time_avg, lead_time_avg=lead_time_avg)

# report generation
def board_metrics(request, board_id):
    print(f">>>>>>>>>>>>>>> board metrics")
    board = Board.objects.get(pk=board_id)
    print(f">>> CALLING calculate_and_store_metrics: {board_id}")
    calculate_and_store_metrics(board)  # Calculate and store metrics for today
    metrics = Metrics.objects.filter(board=board)
    context =  {'board': board, 'metrics': metrics}
    return render(request, 'app_xpresskanban/metrics/board_metrics.html', context)
