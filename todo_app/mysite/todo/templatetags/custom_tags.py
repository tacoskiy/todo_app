import math
from django import template
from django.shortcuts import render
from django.urls import reverse
from todo.models import Task
import datetime
from django.utils import timezone

register = template.Library()

@register.simple_tag
def calc_task_rate():
    now = timezone.now()
    start_of_today = timezone.make_aware(datetime.datetime(now.year, now.month, now.day, 0, 0, 0))
    end_of_today = timezone.make_aware(datetime.datetime(now.year, now.month, now.day, 23, 59, 59))
    totalTasks = Task.objects.filter(due__range=(start_of_today, end_of_today)) 
    completedTasks = totalTasks.filter(isCompleted = True).count()
    totalTasksCount = totalTasks.count()

    if completedTasks == 0 or totalTasksCount == 0:
            result = 0
    else:
        result = math.floor(completedTasks / totalTasksCount * 100)

    return result

@register.simple_tag
def get_remaining_task_count():
     return Task.objects.filter(isCompleted = False).count()

@register.filter
def is_todays_task(due):
    now = timezone.now()
    start_of_today = timezone.make_aware(datetime.datetime(now.year, now.month, now.day, 0, 0, 0))
    end_of_today = timezone.make_aware(datetime.datetime(now.year, now.month, now.day, 23, 59, 59))
    if due == None:
         return False
    else:
        if start_of_today <= due <= end_of_today:
            return True
        else:
            return False
        
@register.filter
def is_over_due(due):
    now = timezone.now()

    if due == None:
         return False
    else:
        if due < now:
            return True
        else:
            return False