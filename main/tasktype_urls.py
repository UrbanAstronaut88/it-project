from django.urls import path
from .views import (
    TaskTypeListView, TaskTypeCreateView,
    TaskTypeUpdateView, TaskTypeDeleteView,
)

urlpatterns = [
    path("", TaskTypeListView.as_view(), name="tasktype-list"),
    path("create/", TaskTypeCreateView.as_view(), name="tasktype-create"),
    path("<int:pk>/update/", TaskTypeUpdateView.as_view(), name="tasktype-update"),
    path("<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="tasktype-delete"),
]
