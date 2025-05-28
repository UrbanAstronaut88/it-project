from django import forms
from .models import Project, Task
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
