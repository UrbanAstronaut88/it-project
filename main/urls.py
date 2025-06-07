from django.urls import path, include
from .views import HomeView, login_view, register_user, logout_view

app_name = "main"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    # Project URLs
    path("projects/", include(("main.project_urls", "main"), namespace="projects")),

    # Task URLs
    path("tasks/", include(("main.task_urls", "main"), namespace="tasks")),

    # Worker URLs
    path("workers/", include(("main.worker_urls", "main"), namespace="workers")),

    # TaskType URLs
    path("tasktypes/", include(("main.tasktype_urls", "main"), namespace="tasktypes")),

    # Auth
    path("login/", login_view, name="login"),
    path("register/", register_user, name="register"),
    path("logout/", logout_view, name="logout"),
]
