from django.urls import path
from .views import (
    TaskListView, TaskDetailView, TaskCreateView,
    TaskUpdateView, TaskDeleteView, task_complete, MyTasksListView,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("create/", TaskCreateView.as_view(), name="task-create"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("<int:pk>/complete/", task_complete, name="task-complete"),
    path("my-tasks/", MyTasksListView.as_view(), name="my-tasks"),
]
