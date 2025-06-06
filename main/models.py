from django.contrib.auth.models import AbstractUser
from django.db import models



class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "Urgent", "Urgent"
        HIGH = "High", "High"
        MEDIUM = "Medium", "Medium"
        LOW = "Low", "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField("Worker", related_name="tasks")
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()

    def __str__(self):
        return self.name
