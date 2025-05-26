from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import Position, Worker, Task, TaskType


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("More info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.fieldsets + (
        ("More info", {"fields": ("position",)}),
    )
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "position"
    )
    list_filter = ("position",)
    search_fields = ("username", "first_name", "last_name", "email")


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "deadline", "priority", "is_completed", "task_type")
    list_filter = ("is_completed", "priority", "task_type", "deadline")
    search_fields = ("name", "description")
    filter_horizontal = ("assignees",)
