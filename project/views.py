from datetime import timedelta, datetime, date
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models.functions import TruncWeek, TruncYear, TruncMonth, TruncDay
from django.db.models import Count, Sum
from django.db.models.query import QuerySet
from django.db import transaction
from django.forms import inlineformset_factory, modelformset_factory, formset_factory
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, UpdateView, WeekArchiveView, MonthArchiveView, DayArchiveView
from django.views.generic.edit import CreateView, FormView
from collections import defaultdict
from .models import Project, Task, Timesheet
from .forms import TaskFormSet, ProjectForm, TimesheetForm
from decimal import Decimal


def get_monday_of_week(given_date):
    # Ensure given_date is a datetime.date object
    if not isinstance(given_date, date):
        raise ValueError("The given_date must be a valid datetime.date object")

    # Calculate the difference between the given date and the Monday of that week
    days_to_monday = given_date.weekday()  # Monday is 0, Sunday is 6
    monday=given_date-timedelta(days=days_to_monday)
    
    return monday


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


class TimesheetView(FormView):
    model = Timesheet
    template_name = 'project/timesheet_formset.html'
    form_class = TimesheetForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user

        week_start = self.kwargs.get('week_start')
        if week_start:
            week_start = date.fromisoformat(week_start)
        else:
            week_start = get_monday_of_week(date.today())
        context['week_start'] = week_start

        end_date = week_start + timedelta(days=6)

        week_data = Timesheet.objects.filter(
            user=user,
            date__range=[week_start, end_date]
        ).select_related('project', 'task').values(
            'project', 'task', 'date', 'hours'
        ).order_by('date')

        grouped_weeks = defaultdict(lambda: defaultdict(dict))
        weekday_map = [
            'monday_hours', 'tuesday_hours', 'wednesday_hours', 
            'thursday_hours', 'friday_hours', 'saturday_hours', 'sunday_hours'
        ]

        for entry in week_data:
            weekday = entry['date'].weekday()
            project = entry['project']
            task = entry['task']
            hours = entry['hours']
            grouped_weeks[project][task][weekday_map[weekday]] = hours

        initial_data = [
            {'project': project, 'task': task, **hours_data}
            for project, tasks in grouped_weeks.items()
            for task, hours_data in tasks.items()
        ]

        TimesheetFormSet = formset_factory(TimesheetForm, extra=0, can_delete=True)
        if self.request.method == 'POST':
            formset = TimesheetFormSet(self.request.POST)
            if formset.is_valid():
                timesheet_entries = []
                for form in formset:
                    for day_key, offset in zip(weekday_map, range(7)):
                        hours = form.cleaned_data.get(day_key)
                        if hours is not None and hours > 0:
                            field_date = week_start + timedelta(days=offset)
                            timesheet_entries.append(
                                Timesheet(
                                    user=user, project=form.cleaned_data['project'], task=form.cleaned_data['task'], date=field_date, hours=hours, start_of_week=week_start
                                    )
                            )
                            
            Timesheet.objects.bulk_create(timesheet_entries)
            # return redirect(reverse('project:timesheet_view', kwargs={'week_start': week_start.isoformat()}))

        else:
            formset = TimesheetFormSet(initial=initial_data)


        context['formset'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        with transaction.atomic():
            formset.save()
            return super().form_valid(form)
    
def timesheet_list_view(request):
    user = request.user
    page = int(request.GET.get('page', 1))  # Get the current page from query params, default is 1
    weeks_per_page = 4  # Number of weeks per page

    # Fetch all timesheets for the user, grouped by week, including related project and task names
    timesheets = Timesheet.objects.filter(user=user).select_related('project', 'task').values(
        'project__name', 'task__name', 'date'
    ).annotate(
        hours=Sum('hours')
    ).order_by('date')

    # Group by week start dates, then by project and task
    grouped_weeks = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    weekday_map = {
        0: 'monday_hours',
        1: 'tuesday_hours',
        2: 'wednesday_hours',
        3: 'thursday_hours',
        4: 'friday_hours',
        5: 'saturday_hours',
        6: 'sunday_hours'
    }

    for entry in timesheets:
        date_of_entry = entry['date']
        weekday = date_of_entry.weekday()
        project_name = entry['project__name']
        task_name = entry['task__name']
        hours = entry['hours']

        # Determine week start (Monday)
        week_start = date_of_entry - timedelta(days=weekday)

        # Group data
        grouped_weeks[week_start][project_name][task_name][weekday_map[weekday]] = hours

    # Convert grouped data to a list of weeks
    weekly_timesheets = []
    for week_start, projects in grouped_weeks.items():
        week_data = {
            'week_start': week_start,
            'projects': [],
            'total_hours': 0,
            'weekday_totals': {day: 0 for day in weekday_map.values()}  # Initialize weekday totals
        }
        
        for project_name, tasks in projects.items():
            project_data = {'project': project_name, 'tasks': [], 'project_total_hours': 0}
            
            for task_name, hours in tasks.items():
                task_data = {'task': task_name, **hours}

                # Sum up task hours for this project
                task_total = sum(hours.get(day, 0) for day in weekday_map.values() if day in hours)
                task_data['task_total_hours'] = task_total
                project_data['project_total_hours'] += task_total

                # Update the weekly totals for each day
                for day, day_hours in hours.items():
                    week_data['weekday_totals'][day] += day_hours
                project_data['tasks'].append(task_data)
            
            # Add project total to week total
            week_data['total_hours'] += project_data['project_total_hours']
            week_data['projects'].append(project_data)

        weekly_timesheets.append(week_data)

    # Order weeks by start date for pagination
    weekly_timesheets.sort(key=lambda x: x['week_start'], reverse=True)

    # Paginate weeks
    paginator = Paginator(weekly_timesheets, weeks_per_page)
    paginated_weeks = paginator.get_page(page)

    context = {
        'weekly_timesheets': paginated_weeks,
        'page': page,
        'has_next': paginated_weeks.has_next(),
        'has_previous': paginated_weeks.has_previous(),
        'next_page_number': paginated_weeks.next_page_number() if paginated_weeks.has_next() else None,
        'previous_page_number': paginated_weeks.previous_page_number() if paginated_weeks.has_previous() else None
    }


class TimesheetListView(ListView):
    model = Timesheet
    template_name = 'project/timesheet_listview.html'
    context_object_name = 'timesheets'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['daily_timesheets'] = Timesheet.daily.all()
        context["weekly_timesheets"] = Timesheet.weekly.all()
        context["monthly_timesheets"] = Timesheet.monthly.all()
        return context
    
    def get_queryset(self):
        # Fetch all timesheets for the user, grouped by week, including related project and task names
        return Timesheet.objects.filter(user=self.request.user).order_by('date')
    

class WeeklyTimesheetList(ListView):
    model = Timesheet
    template_name = 'project/timesheet_list_weekly.html'
    context_object_name = 'timesheets'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["weekly_timesheets"] = Timesheet.weekly.all()
        return context
    
    def get_queryset(self):
        # Fetch all timesheets for the user, grouped by week, including related project and task names
        return Timesheet.objects.filter(user=self.request.user).order_by('-date')
    

class MonthlyTimesheetList(ListView):
    model = Timesheet
    template_name = 'project/timesheet_list_monthly.html'
    context_object_name = 'timesheets'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["monthly_timesheets"] = Timesheet.monthly.all()
        return context
    
    def get_queryset(self):
        # Fetch all timesheets for the user, grouped by month, including related project and task names
        return Timesheet.objects.filter(user=self.request.user).order_by('-date')
    

class DailyTimesheetList(ListView):
    model = Timesheet
    template_name = 'project/timesheet_list_daily.html'
    context_object_name = 'timesheets'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['daily_timesheets'] = Timesheet.daily.all()
        return context
    
    def get_queryset(self):
        # Fetch all timesheets for the user, grouped by week, including related project and task names
        return Timesheet.objects.filter(user=self.request.user).order_by('-date')


class WeeklyTimesheetView(WeekArchiveView):
    model = Timesheet
    context_object_name = 'timesheets'
    date_field = 'date'
    week_format = "%W"
    allow_future = True
    allow_empty=True
    template_name = 'project/timesheet_archive_week.html'
    TimesheetFormSet = formset_factory(TimesheetForm, extra=0, can_delete=True)
    
    def get_week_start(self):
        year_week_key = str(self.kwargs["year"]) + "-W" + str(self.kwargs["week"])
        week_start = datetime.strptime(year_week_key + '-1', "%Y-W%W-%w")
        return week_start
    
    def get_weekly_timesheet_data(self, user, week_start):
        grouped_weeks = defaultdict(lambda: defaultdict(dict))
        weekday_map = [
            'monday_hours', 'tuesday_hours', 'wednesday_hours', 
            'thursday_hours', 'friday_hours', 'saturday_hours', 'sunday_hours'
        ]
        weekly_entries = Timesheet.objects.filter(
            user=user,
            start_of_week=week_start,
        ).select_related('project', 'task').values(
            'project', 'task', 'date'
        ).annotate(total_hours=Sum('hours')).order_by('date')
        
        for entry in weekly_entries:
            weekday = entry['date'].weekday()
            project = entry['project']
            task = entry['task']
            hours = entry['total_hours']
            grouped_weeks[project][task][weekday_map[weekday]] = hours

        initial_data = [
            {'project': project, 'task': task, **hours_data}
            for project, tasks in grouped_weeks.items()
            for task, hours_data in tasks.items()
        ]
        return initial_data

    def get_weekly_timesheet_formsets(self, user, week_start):
        weekly_timesheet_data = self.get_weekly_timesheet_data(user=user, week_start=week_start)
        formset = self.TimesheetFormSet(initial=weekly_timesheet_data)
        return formset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_start = self.get_week_start()
        context["weekly_timesheets"] = Timesheet.weekly.filter(start_of_week=week_start)
        user = self.request.user
        formset = self.get_weekly_timesheet_formsets(user, week_start)
        context["formset"] = formset
        return context  
    
    def get_queryset(self):
        # Fetch all timesheets for the user, grouped by week, including related project and task names
        week_start = self.get_week_start()
        return Timesheet.objects.filter(user=self.request.user, start_of_week=week_start).order_by('date')


class MonthlyTimesheetView(MonthArchiveView):
    model = Timesheet
    context_object_name = 'timesheets'
    date_field = 'date'
    month_format = "%M"
    allow_future = True
    allow_empty = True
    template_name = 'project/timesheet_archive_month.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['daily_timesheets'] = Timesheet.daily.all()
        context["weekly_timesheets"] = Timesheet.weekly.all()
        context["monthly_timesheets"] = Timesheet.monthly.all()
        return context  
    
    def get_queryset(self):
        # Fetch all timesheets for the user, grouped by month, including related project and task names
        # b = str(self.kwargs["year"]) + "-" + str(self.kwargs["month"])
        # r = datetime.strptime(b + '-1', "%Y-%M")
        return Timesheet.objects.filter(user=self.request.user).order_by('date')
    
    