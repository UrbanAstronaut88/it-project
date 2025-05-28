from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView
)
from main.forms import ProjectForm
from main.models import Project, Task


class ProjectListView(ListView):
    model = Project
    template_name = "main/project_list.html"
    context_object_name = "projects"


class ProjectDetailView(DetailView):
    model = Project
    template_name = "main/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.filter(project=self.get_object())
        return context


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "main/project_form.html"
    success_url = reverse_lazy("main:project-list")


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "main/project_form.html"
    success_url = reverse_lazy("main:project-list")


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "main/project_confirm_delete.html"
    success_url = reverse_lazy("main:project-list")


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


class TaskDetailView(DetailView):
    model = Task
    template_name = "main/task_detail.html"
    context_object_name = "task"


class TaskUpdateView(UpdateView):
    model = Task
    fields = [
        "name",
        "description",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
        "assignees",
    ]
    template_name = "main/task_form.html"
    success_url = reverse_lazy("main:task-list")


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "main/task_confirm_delete.html"
    success_url = reverse_lazy("main:task-list")
