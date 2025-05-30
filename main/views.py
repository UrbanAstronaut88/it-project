from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView
)
from main.forms import ProjectForm, TaskForm, RegisterForm
from main.models import Project, Task, TaskType, Worker


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


class WorkerDetailView(DetailView):
    model = User
    template_name = "main/worker_detail.html"
    context_object_name = "worker"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.object
        context["assigned_tasks"] = worker.tasks.all()
        return context


class WorkerCreateView(CreateView):
    model = User
    fields = ("username", "first_name", "last_name", "email", "position")
    template_name = "main/worker_form.html"
    success_url = reverse_lazy("main:worker-list")


class WorkerUpdateView(UpdateView):
    model = User
    fields = ("username", "first_name", "last_name", "email", "position")
    template_name = "main/worker_form.html"
    success_url = reverse_lazy("main:worker-list")


class WorkerDeleteView(DeleteView):
    model = User
    template_name = "main/worker_confirm_delete.html"
    success_url = reverse_lazy("main:worker-list")


class TaskListView(ListView):
    model = Task
    template_name = "main/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = Task.objects.select_related("project").prefetch_related("assignees")
        project_id = self.request.GET.get("project")
        assignee_id = self.request.GET.get("assignee")

        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if assignee_id:
            queryset = queryset.filter(assignees__id=assignee_id)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.all()
        context["workers"] = Worker.objects.all()
        context["selected_project_id"] = self.request.GET.get("project", "")
        context["selected_assignee_id"] = self.request.GET.get("assignee", "")
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = "main/task_detail.html"
    context_object_name = "task"


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "main/task_form.html"
    success_url = reverse_lazy("main:task-list")

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get("project")
        if project_id:
            initial["project"] = project_id
        return initial


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "main/task_form.html"
    success_url = reverse_lazy("main:task-list")


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "main/task_confirm_delete.html"
    success_url = reverse_lazy("main:task-list")


#@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user in task.assignees.all():
        if not task.is_completed:
            task.is_completed = True
            task.save()
            messages.success(request, "Task marked as completed.")
        else:
            messages.info(request, "Task was already completed.")
    else:
        messages.error(request, "You are not assigned to this task.")
    return redirect("main:worker-detail", pk=request.user.pk)


class TaskTypeListView(ListView):
    model = TaskType
    template_name = "main/tasktype_list.html"
    context_object_name = "task_types"


class TaskTypeCreateView(CreateView):
    model = TaskType
    fields = ["name"]
    template_name = "main/tasktype_form.html"
    success_url = reverse_lazy("main:tasktype-list")


class TaskTypeUpdateView(UpdateView):
    model = TaskType
    fields = ["name"]
    template_name = "main/tasktype_form.html"
    success_url = reverse_lazy("main:tasktype-list")


class TaskTypeDeleteView(DeleteView):
    model = TaskType
    template_name = "main/tasktype_confirm_delete.html"
    success_url = reverse_lazy("main:tasktype-list")


class MyTasksListView(ListView):
    model = Task
    template_name = "main/my_tasks.html"
    context_object_name = "tasks"
    #paginate_by = 3

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user)


#registration view
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # < автоматический вход после регистрации(глянуть документацию)
            return redirect("main:project-list")

    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

