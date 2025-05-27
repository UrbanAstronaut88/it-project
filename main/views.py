from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from main.models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "main/project_list.html"
    context_object_name = "projects"


class HomeView(TemplateView):
    template_name = "main/home.html"
