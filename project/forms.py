# forms.py
from django import forms
from .models import Task, Project
from django.forms import modelformset_factory

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'due_date', 'completed']

# Create a formset for multiple tasks
TaskFormSet = modelformset_factory(Task, form=TaskForm, extra=1)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'projectmanager', 
            'name', 
            'description', 
            'start_date', 
            'end_date', 
            'project_status', 
            'businessunit'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round', 'placeholder': 'Enter project name'}),
            'description': forms.Textarea(attrs={'class': 'w3-input w3-border w3-round', 'rows': 3, 'placeholder': 'Enter project description'}),
            'start_date': forms.DateInput(attrs={'class': 'w3-input w3-border w3-round', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'w3-input w3-border w3-round', 'type': 'date'}),
            'project_status': forms.Select(attrs={'class': 'w3-select w3-border w3-round'}),
            'businessunit': forms.SelectMultiple(attrs={'class': 'w3-select w3-border w3-round'}),
            'projectmanager': forms.Select(attrs={'class': 'w3-input w3-border w3-round'}),
        }
