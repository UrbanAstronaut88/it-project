from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from main.models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "main/project_list.html"
    context_object_name = "projects"


class HomeView(TemplateView):
    template_name = "main/home.html"


User = get_user_model()

class WorkerListView(ListView):
    model = User
    template_name = "main/worker_list.html"
    context_object_name = "workers"
