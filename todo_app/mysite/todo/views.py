from django.utils import timezone
import datetime
import math
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

from django.db.models import Q
from django.contrib import messages

from .forms import TaskCreateForm
from .models import Task

from django.db.models import F

from django.urls import reverse
from urllib.parse import urlencode

class TaskListView(generic.ListView):
    model = Task

    def get_queryset(self):
        queryset = Task.objects.order_by(F('due').asc(nulls_last=True))
        query = self.request.GET.get('query')

        now = timezone.now()
        start_of_today = timezone.make_aware(datetime.datetime(now.year, now.month, now.day, 0, 0, 0))
        end_of_today = timezone.make_aware(datetime.datetime(now.year, now.month, now.day, 23, 59, 59))


        filters = Q()

        if query:
            filters &= Q(title__icontains=query)

        is_completed = self.request.GET.get('isCompleted', 'false')

        if is_completed == 'true':
            filters &= Q(isCompleted=True)
        elif is_completed == 'false':
            filters &= Q(isCompleted=False)

        is_todays_task = self.request.GET.get('isTodaysTask')

        if is_todays_task == 'true':
            filters &= Q(due__range=(start_of_today, end_of_today))
        elif is_todays_task == 'false':
            filters &= ~Q(due__range=(start_of_today, end_of_today))

        is_over_due = self.request.GET.get('isOverDue')

        if is_over_due == 'true':
            filters &= Q(due__lt=now)
        elif is_over_due == 'false':
            filters &= ~Q(due__lt=now)

        is_Stared = self.request.GET.get('isStared')

        if is_Stared == 'true':
            filters &= Q(isStared=True)
        elif is_Stared == 'false':
            filters &= Q(isStared=False)

        is_none_due = self.request.GET.get('isNoneDue')

        if is_none_due == 'true':
            filters &= Q(due__isnull = True)
        elif is_none_due == 'false':
            filters &= Q(due__isnull = False)

        sort_by = self.request.GET.get('sortBy')

        if sort_by == 'complete_date':
            queryset = Task.objects.order_by(('completeDate'))

        messages.add_message(self.request, messages.INFO, query)
        return queryset.filter(filters)

    
class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy('todo:task_list')

def toggle_task_completion(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.isCompleted = not task.isCompleted
    task.completeDate = timezone.now()
    task.save()

    
    url = reverse('todo:task_list')
    query_params = urlencode({'isCompleted': 'true', 'sortBy': 'complete_date'})

    if task.isCompleted == False:
        return redirect(f"{url}?{query_params}")
    else:
        return redirect('todo:task_list')
    

class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy('todo:task_list')