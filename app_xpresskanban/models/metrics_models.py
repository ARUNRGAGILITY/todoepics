from .all_imports import *

from .core_models import *
from .delivery_models import *
from .metrics_models import *
class CardMovement(models.Model):
    card = TreeForeignKey('app_xpresskanban.CORE_HSDB', on_delete=models.SET_NULL, null=True, blank=True, related_name="cardmovement")
    source_column = models.ForeignKey(BoardColumns, on_delete=models.CASCADE, related_name='source_movements', null=True, blank=True,default='Start')
    target_column = models.ForeignKey(BoardColumns, on_delete=models.CASCADE, related_name='target_movements', null=True, blank=True,default='Start')
    moved_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="xpress_cardmovement_author")
    # card metrics
    time_entered = models.DateTimeField(auto_now_add=True)
    time_exited = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(null=True, blank=True, default=timedelta(seconds=0))
    def __str__(self):
        return self.card.title


#
#
# Delay
#
#
class Delay(models.Model):
    card = TreeForeignKey('app_xpresskanban.CORE_HSDB', on_delete=models.SET_NULL, null=True, blank=True, related_name="card_delays")
    column = models.ForeignKey(BoardColumns, on_delete=models.CASCADE, related_name='delay_movements', null=True, blank=True,default='Start')
    delay_type = models.CharField(max_length=100,null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    delay_duration = models.DurationField(null=True, blank=True)


#
#
# CFD data 
#
#
class CFDData(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE,null=True, blank=True)
    date = models.DateField(null=True, blank=True)      
    cfd_data = models.TextField(null=True, blank=True,)  



class Metrics(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE,null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    cycle_time_avg = models.FloatField(null=True, blank=True)
    lead_time_avg = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.board.title