# forms.py
from datetime import timedelta
from django import forms
from django.forms import modelformset_factory
from django_select2 import forms as s2forms
from .models import Timesheet, Project, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'name', 'description', 'due_date', 'completed']

# Create a formset for multiple tasks
TaskFormSet = modelformset_factory(Task, form=TaskForm, extra=1)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'id',
            'projectmanager',             
            'name', 
            'description', 
            'start_date', 
            'end_date', 
            'project_status', 
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round', 'placeholder': 'Enter project name'}),
            'description': forms.Textarea(attrs={'class': 'w3-input w3-border w3-round', 'rows': 3, 'placeholder': 'Enter project description'}),
            'start_date': forms.DateInput(attrs={'class': 'w3-input w3-border w3-round', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'w3-input w3-border w3-round', 'type': 'date'}),
            'project_status': forms.Select(attrs={'class': 'w3-select w3-border w3-round'}),
            'projectmanager': forms.Select(attrs={'class': 'w3-input w3-border w3-round'}),
        }


class WeekTimesheetForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    task = forms.ModelChoiceField(queryset=Task.objects.all())
    monday_hours = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    tuesday_hours = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    wednesday_hours = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    thursday_hours = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    friday_hours = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    
    def save(self, user, week_start_date):
        project = self.cleaned_data['project']
        task = self.cleaned_data['task']
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        for i, day in enumerate(days):
            hours = self.cleaned_data.get(f'{day}_hours')
            if hours:
                Timesheet.objects.create(
                    user=user,
                    project=project,
                    task=task,
                    date=week_start_date + timedelta(days=i),
                    hours=hours
                )
