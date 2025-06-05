from django.urls import path
from .views import (
    WorkerListView, WorkerDetailView,
    WorkerCreateView, WorkerUpdateView, WorkerDeleteView,
)

urlpatterns = [
    path("", WorkerListView.as_view(), name="worker-list"),
    path("create/", WorkerCreateView.as_view(), name="worker-create"),
    path("<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
]
