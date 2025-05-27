from django.urls import path
from .views import ProjectListView, HomeView, WorkerListView

app_name = "main"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
]
