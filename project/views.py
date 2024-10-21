from datetime import timedelta, datetime
from django.contrib.auth.models import User
from django.db.models import Sum
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import CreateView, FormView
from .models import Project, Task, Timesheet
from .forms import TaskFormSet, ProjectForm, TimesheetForm, BaseWeekTimesheetFormSet

# Create your views here.
def get_week_start(date):
    # Function to get the start of the week (Monday)
    start = date - timedelta(days=date.weekday())
    return start


class ProjectListView(ListView):
    model = Project
    template_name = 'project/project_list.html'  
    

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_form.html'
    success_url = reverse_lazy('project_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['task_formset'] = TaskFormSet(self.request.POST)
        else:
            context['task_formset'] = TaskFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        task_formset = context['task_formset']
        if task_formset.is_valid():
            self.object = form.save()  # Save the project instance
            task_formset.instance = self.object  # Link tasks to the project
            task_formset.save()  # Save all tasks
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_form.html'  
    success_url = reverse_lazy('project:project_list') 
    
    # Override get_context_data to add custom context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['task_formset'] = TaskFormSet(self.request.POST, instance=self.object)
        else:
            context['task_formset'] = TaskFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        task_formset = context['task_formset']
        if task_formset.is_valid():
            self.object = form.save()  # Save the project instance
            task_formset.instance = self.object  # Link tasks to the project
            task_formset.save()  # Save all tasks
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


def timesheet_view(request):
    # Get current date and handle week navigation
    week_offset = int(request.GET.get('week_offset', 0))
    current_date = datetime.today() + timedelta(weeks=week_offset)
    week_start = get_week_start(current_date) # Function to get the start of the week (Monday)
    end_week = week_start + timedelta(days=4)
    
    week_data = (
        Timesheet.objects
        .filter(date__range=[week_start, end_week])
        .order_by('date')
        .values('user', 'project', 'task', 'date')
        .annotate(hours=Sum('hours'))
    )
    
    # Create the formset factory
    TimesheetFormSet = inlineformset_factory(
        User, 
        Timesheet,
        form=TimesheetForm,
        formset=BaseWeekTimesheetFormSet,
        fields=('user', 'project', 'task'),
        extra=week_data.count(),
        can_delete=True
    )
    print(week_data)
    print("count: ",week_data.count())
    
    if request.method == 'POST':
        formset = TimesheetFormSet(request.POST, week_data=week_data)
        if formset.is_valid():
            formset.save(user=request.user, week_start=week_start)
            return redirect('project:timesheet_view')
    else:
        formset = TimesheetFormSet(week_data=week_data)
    
    context = {
        'formset': formset,
        'week_start_date': week_start,
        'week_offset': week_offset
    }
    return render(request, 'project/timesheet_formset.html', context)
