from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import Position, Worker, Task, TaskType, Project


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("first_name", "last_name", "position",)}),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "position"
    )
    list_filter = ("position", "is_staff", "is_superuser")
    search_fields = ("username", "first_name", "last_name", "position__name")


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "deadline", "is_completed", "priority", "task_type",)
    list_filter = ("is_completed", "priority", "project", "deadline")
    search_fields = ("name", "description")
    filter_horizontal = ("assignees",)
    autocomplete_fields = ("task_type",)
    date_hierarchy = "deadline"
    fieldsets = (
        (None, {"fields": ("name",
                           "description",
                           "deadline",
                           "priority",
                           "project",
                           "assignees",
                           "task_type",
                           )
                }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "deadline",)
    search_fields = ("name",)
