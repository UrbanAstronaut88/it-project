from django.contrib.auth import get_user_model
from django.views.generic import ListView, TemplateView
from main.models import Project, Task


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


class TaskListView(ListView):
    model = Task
    template_name = "main/task_list.html"
    context_object_name = "tasks"
