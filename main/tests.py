import datetime

from django.test import TestCase
from main.models import Project, TaskType, Task, Worker
from django.contrib.auth import get_user_model

User = get_user_model()


class ModelsTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Website Redesign",
            deadline=datetime.date.today() + datetime.timedelta(days=30),
        )
        self.task_type = TaskType.objects.create(name="Development")
        self.worker = Worker.objects.create_user(
            username="John Doe",
            password="testpass123",
            first_name="John",
            last_name="Doe"
        )

    def test_task_type_creation(self):
        self.assertEqual(str(self.task_type), "Development")

    def test_worker_creation(self):
        self.assertEqual(str(self.worker), "John Doe")

    def test_task_creation_and_relations(self):
        task = Task.objects.create(
            name="Create homepage",
            description="Design and build homepage",
            is_completed=False,
            project=self.project,
            task_type=self.task_type,
            deadline=datetime.date.today() + datetime.timedelta(days=30),
        )
        task.assignees.add(self.worker)

        self.assertEqual(str(task), "Create homepage")
        self.assertEqual(task.project.name, "Website Redesign")
        self.assertEqual(task.task_type.name, "Development")
        self.assertIn(self.worker, task.assignees.all())

    def test_project_creation(self):
        project = Project.objects.create(
            name="New Project",
            description="A test project",
            deadline=datetime.date.today() + datetime.timedelta(days=30),
        )
        self.assertEqual(project.name, "New Project")
        self.assertEqual(str(project), "New Project")

    def test_assign_worker_to_task(self):
        task = Task.objects.create(
            name="Backend API",
            description="Create API endpoints",
            deadline=datetime.date.today() + datetime.timedelta(days=5),
            priority="Medium",
            project=self.project,
            task_type=self.task_type
        )
        task.assignees.add(self.worker)
        self.assertIn(self.worker, task.assignees.all())

    def test_cascade_delete_project_deletes_tasks(self):
        task = Task.objects.create(
            name="To be deleted",
            description="This task will be deleted with project",
            deadline=datetime.date.today(),
            project=self.project,
            task_type=self.task_type
        )
        self.assertEqual(Task.objects.count(), 1)
        self.project.delete()
        self.assertEqual(Task.objects.count(), 0)

    def test_filter_tasks_by_assignee(self):
        task1 = Task.objects.create(
            name="Task 1",
            description="Desc",
            deadline=datetime.date.today(),
            project=self.project,
            task_type=self.task_type
        )
        task2 = Task.objects.create(
            name="Task 2",
            description="Desc",
            deadline=datetime.date.today(),
            project=self.project,
            task_type=self.task_type
        )
        task1.assignees.add(self.worker)

        assigned_tasks = Task.objects.filter(assignees=self.worker)
        self.assertIn(task1, assigned_tasks)
        self.assertNotIn(task2, assigned_tasks)

    def test_filter_incomplete_tasks(self):
        Task.objects.create(
            name="Incomplete Task",
            description="Still in progress",
            is_completed=False,
            deadline=datetime.date.today(),
            project=self.project,
            task_type=self.task_type
        )
        Task.objects.create(
            name="Completed Task",
            description="Done",
            is_completed=True,
            deadline=datetime.date.today(),
            project=self.project,
            task_type=self.task_type
        )

        incomplete_tasks = Task.objects.filter(is_completed=False)
        self.assertEqual(incomplete_tasks.count(), 1)
        self.assertEqual(incomplete_tasks.first().name, "Incomplete Task")
