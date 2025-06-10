from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('task_list/', views.TaskListView.as_view(), name='task_list'),
    path('task_create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task_list/<int:task_id>/toggle/', views.toggle_task_completion, name='toggle_task_completion'),
    path('task_update/<int:pk>/', views.TaskUpdateView.as_view(), name='task_update'),
]