from django.urls import path
from .views import (
    HomeView,

    # Projects
    ProjectListView, ProjectDetailView, ProjectCreateView,
    ProjectUpdateView, ProjectDeleteView,

    # Tasks
    TaskListView, TaskDetailView, TaskCreateView,
    TaskUpdateView, TaskDeleteView, task_complete, MyTasksListView,

    # Workers
    WorkerListView, WorkerDetailView, WorkerCreateView,
    WorkerUpdateView, WorkerDeleteView,

    # TaskTypes
    TaskTypeListView, TaskTypeCreateView,
    TaskTypeUpdateView, TaskTypeDeleteView,

    # Auth
    login_view, register_user, logout_view,
)

app_name = "main"

urlpatterns = [
    # Home
    path("", HomeView.as_view(), name="home"),

    # Projects
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("projects/create/", ProjectCreateView.as_view(), name="project-create"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"),
    path("projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"),

    # Tasks
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/complete/", task_complete, name="task-complete"),

    # My Tasks
    path("my-tasks/", MyTasksListView.as_view(), name="my-tasks"),

    # Workers
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),

    # Task Types
    path("tasktypes/", TaskTypeListView.as_view(), name="tasktype-list"),
    path("tasktypes/create/", TaskTypeCreateView.as_view(), name="tasktype-create"),
    path("tasktypes/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="tasktype-update"),
    path("tasktypes/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="tasktype-delete"),

    # Authentication
    path("login/", login_view, name="login"),
    path("register/", register_user, name="register"),
    path("logout/", logout_view, name="logout"),
]
