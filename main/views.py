from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
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
from main.forms import ProjectForm, TaskForm, LoginForm, SignUpForm
from main.models import Project, Task, TaskType, Worker


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "main/project_list.html"
    context_object_name = "projects"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context["paginator"]
        page_obj = context["page_obj"]
        projects = context["projects"]

        if not projects and int(self.request.GET.get("page", 1)) > 1:
            context["projects"] = paginator.page(paginator.num_pages)

        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "main/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.filter(project=self.get_object())
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "main/project_form.html"
    success_url = reverse_lazy("main:projects:project-list")


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "main/project_form.html"
    success_url = reverse_lazy("main:projects:project-list")


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "main/project_confirm_delete.html"
    success_url = reverse_lazy("main:projects:project-list")


class HomeView(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_workers"] = Worker.objects.count()
        context["num_tasks"] = Task.objects.count()
        context["num_projects"] = Project.objects.count()
        return context


User = get_user_model()
class WorkerListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "main/worker_list.html"
    context_object_name = "workers"
    paginate_by = 6


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "main/worker_detail.html"
    context_object_name = "worker"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.object
        context["assigned_tasks"] = worker.tasks.all()
        return context


class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = ("username", "first_name", "last_name", "email", "position")
    template_name = "main/worker_form.html"
    success_url = reverse_lazy("main:workers:worker-list")


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ("username", "first_name", "last_name", "email", "position")
    template_name = "main/worker_form.html"
    success_url = reverse_lazy("main:workers:worker-list")


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "main/worker_confirm_delete.html"
    success_url = reverse_lazy("main:workers:worker-list")


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "main/task_list.html"
    context_object_name = "tasks"
    paginate_by = 2

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


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "main/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "main/task_form.html"
    success_url = reverse_lazy("main:tasks:task-list")

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get("project")
        if project_id:
            initial["project"] = project_id
        return initial


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "main/task_form.html"
    success_url = reverse_lazy("main:tasks:task-list")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "main/task_confirm_delete.html"
    success_url = reverse_lazy("main:tasks:task-list")


@login_required
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
    return redirect("main:workers:worker-detail", pk=request.user.pk)


class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    template_name = "main/tasktype_list.html"
    context_object_name = "task_types"


class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    fields = ["name"]
    template_name = "main/tasktype_form.html"
    success_url = reverse_lazy("main:tasktypes:tasktype-list")


class TaskTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskType
    fields = ["name"]
    template_name = "main/tasktype_form.html"
    success_url = reverse_lazy("main:tasktypes:tasktype-list")


class TaskTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskType
    template_name = "main/tasktype_confirm_delete.html"
    success_url = reverse_lazy("main:tasktypes:tasktype-list")


class MyTasksListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "main/my_tasks.html"
    context_object_name = "tasks"
    #paginate_by = 3

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user)


# class RegisterView(CreateView):
#     form_class = UserRegisterForm
#     template_name = "registration/register.html"
#     success_url = reverse_lazy("login")

#LOGIN
def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = "Invalid credentials"
        else:
            msg = 'Error validating the form'

    return render(request, "registration/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = "Form is not valid"
    else:
        form = SignUpForm()

    return render(request, "registration/register.html", {"form": form, "msg": msg, "success": success})


#Logout
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("main:login")
    else:
        return HttpResponse("Logout only via POST", status=405)
