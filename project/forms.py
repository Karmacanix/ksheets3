# forms.py
from datetime import timedelta, datetime, date, time
from django.contrib.auth.models import User
from django import forms
from django.forms import inlineformset_factory, formset_factory, modelformset_factory
from django_select2.forms import ModelSelect2Widget
from .models import Timesheet, Project, Task
from django.forms.models import BaseInlineFormSet
from collections import defaultdict


class CustomDecimalWidget(forms.NumberInput):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.get('attrs', {})
        attrs.update({'step': '0.5', 'class': 'w3-input w3-border w3-round'})
        kwargs['attrs'] = attrs
        super().__init__(*args, **kwargs)
        

class CustomDecimalField(forms.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = CustomDecimalWidget()
        super().__init__(*args, **kwargs)


class BaseWeekTimesheetFormSet(BaseInlineFormSet):

    def __init__(self, *args, week_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if week_data:
            # Dictionary to group entries by (project, task) and store the day hours
            grouped_data = defaultdict(lambda: {
                'monday_hours': 0,
                'tuesday_hours': 0,
                'wednesday_hours': 0,
                'thursday_hours': 0,
                'friday_hours': 0
            })
            
            for data in week_data:
                # Determine the weekday of the date
                weekday = data['date'].weekday()
                
                # Get the corresponding field for the day
                weekday_map = {
                    0: 'monday_hours',
                    1: 'tuesday_hours',
                    2: 'wednesday_hours',
                    3: 'thursday_hours',
                    4: 'friday_hours'
                }
                
                # Only process weekdays (0 to 4)
                if weekday in weekday_map:
                    # Group by project and task
                    key = (data['project'], data['task'])
                    grouped_data[key][weekday_map[weekday]] += data['hours']
                    grouped_data[key].update({
                        'user': data['user'],
                        'project': data['project'],
                        'task': data['task'],
                    })
            
            # Now use the grouped data to populate the forms
            for form, (key, day_hours) in zip(self.forms, grouped_data.items()):
                form.initial['user'] = day_hours['user']
                form.initial['project'] = day_hours['project']
                form.initial['task'] = day_hours['task']
                
                # Populate the weekday hours fields
                form.initial['monday_hours'] = day_hours['monday_hours']
                form.initial['tuesday_hours'] = day_hours['tuesday_hours']
                form.initial['wednesday_hours'] = day_hours['wednesday_hours']
                form.initial['thursday_hours'] = day_hours['thursday_hours']
                form.initial['friday_hours'] = day_hours['friday_hours']


    def save(self, user=None, week_start=None, commit=True):
        """
        Saves the timesheet entries, one per day with the relevant hours.
        `start_date` should be a Monday to correctly align the days.
        """
        if week_start is None:
            raise ValueError("You must provide a week_start (Monday).")

        timesheet_entries = []
        for form in self.forms:
            if form.cleaned_data:
                project = form.cleaned_data.get('project')
                task = form.cleaned_data.get('task')
                
                # Loop through each day of the week (Monday to Friday)
                for i, day_field in enumerate(['monday_hours', 'tuesday_hours', 'wednesday_hours', 'thursday_hours', 'friday_hours']):
                    hours = form.cleaned_data.get(day_field)
                    if hours:  # Only save if hours are entered
                        date = week_start + timedelta(days=i)  # Calculate the correct date
                        timesheet_entry = Timesheet(
                            user=user,
                            project=project,
                            task=task,
                            date=date,
                            hours=hours
                        )
                        timesheet_entries.append(timesheet_entry)
        
        if commit:
            Timesheet.objects.bulk_create(timesheet_entries)  # Save all entries at once
        
        return timesheet_entries


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
            'customer',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round', 'placeholder': 'Enter project name'}),
            'description': forms.Textarea(attrs={'class': 'w3-input w3-border w3-round', 'rows': 3, 'placeholder': 'Enter project description'}),
            'start_date': forms.DateInput(attrs={'class': 'w3-input w3-border w3-round', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'w3-input w3-border w3-round', 'type': 'date'}),
            'project_status': forms.Select(attrs={'class': 'w3-select w3-border w3-round'}),
            'projectmanager': forms.Select(attrs={'class': 'w3-input w3-border w3-round'}),
            'customer': forms.Select(attrs={'class': 'w3-select w3-border w3-round'}),
        }


# Formset for Task management
TaskFormSet = inlineformset_factory(
    Project, Task,
    fields=['project', 'name', 'description', 'due_date', 'completed',],
    extra=1,  # Number of extra task forms to show by default
    can_delete=True,  # Allow task deletion
    widgets = {
        'due_date': forms.DateInput(attrs={'class': 'w3-input w3-border w3-round', 'type': 'date'}),
        'name': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round',}),
        'description': forms.Textarea(attrs={'class': 'w3-input w3-border w3-round', 'rows': 1, }),  
        'completed': forms.CheckboxInput(attrs={'class': 'w3-input w3-border w3-round', }),
        'delete': forms.CheckboxInput(attrs={'class': 'w3-input w3-border w3-round'}),
        }
)


class TimesheetForm(forms.ModelForm):
    monday_hours = CustomDecimalField(min_value=0, max_value=24, max_digits=5, decimal_places=2, required=False)
    tuesday_hours = CustomDecimalField(min_value=0, max_value=24, max_digits=5, decimal_places=2, required=False)
    wednesday_hours = CustomDecimalField(min_value=0, max_value=24, max_digits=5, decimal_places=2, required=False)
    thursday_hours = CustomDecimalField(min_value=0, max_value=24, max_digits=5, decimal_places=2, required=False)
    friday_hours = CustomDecimalField(min_value=0, max_value=24, max_digits=5, decimal_places=2, required=False)
    
    class Meta:
        model = Timesheet
        fields = ['project', 'task']
        widgets = {
            'project': forms.Select(attrs={'class': 'w3-select w3-border w3-round'}),
            'task': forms.Select(attrs={'class': 'w3-select w3-border w3-round'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        # Add any additional validation for hours if needed here
        return cleaned_data
    
    def save(self, commit=True):
        return super().save(commit=commit)