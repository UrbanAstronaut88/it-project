from django.urls import path
from .views import ProjectListView


app_name = "main"
urlpatterns = [
    path("projects/", ProjectListView.as_view(), name="project-list"),
]