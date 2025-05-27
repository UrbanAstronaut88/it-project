from django.urls import path
from .views import ProjectListView, HomeView


app_name = "main"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
]
