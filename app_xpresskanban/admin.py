from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(TYPE_HSDB)

class COREHSDBAdmin(admin.ModelAdmin):
    list_display = ['board', 'column', 'title', 'project',]
admin.site.register(CORE_HSDB, COREHSDBAdmin)

admin.site.register(BaseType)
admin.site.register(BaseState)
admin.site.register(BasePriority)

admin.site.register(Project)
admin.site.register(Product)
admin.site.register(Service)
admin.site.register(Solution)
admin.site.register(ValueStream)
admin.site.register(Organization)
admin.site.register(Board)

class BoardColumnsAdmin(admin.ModelAdmin):
    list_display = ['title', 'wip_limit', 'cycle_time_column']
admin.site.register(BoardColumns, BoardColumnsAdmin)
admin.site.register(BoardHistory)
admin.site.register(VisionMissionValueSRI)


class CardMovementAdmin(admin.ModelAdmin):
    list_display = ['author', 'card', 'source_column', 'target_column', 'time_entered', 'time_exited', 'time_spent']
admin.site.register(CardMovement, CardMovementAdmin)
class MetricsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Metrics._meta.get_fields()]
admin.site.register(Metrics, MetricsAdmin)

class SwimlaneAdmin(admin.ModelAdmin):
    list_display = ['position' , 'board', 'title', 'description']
admin.site.register(Swimlane, SwimlaneAdmin)

