import datetime
from django.contrib.auth.models import User
from django.db import models

from django.db.models import Sum, F, Value
from django.urls import reverse
from django.db.models.functions import TruncWeek, TruncMonth, TruncDay
from django.db.models.functions import TruncDay
from customer.models import Customer


# Create your models here.
class Project(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define an AutoField as the primary key
    projectmanager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projectmanager")
    name = models.CharField(max_length=254)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='projects')
    PROJECT_STATUS_CHOICES = (
        ('N', 'New'),
        ('W', 'In Progress'),
        ('H', 'On Hold'),
        ('C', 'Closed'),
    )
    project_status = models.CharField(
        max_length=1,
        choices=PROJECT_STATUS_CHOICES,
        default='N',
        verbose_name="Status"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class WeeklyTimesheetManager(models.Manager):
    def get_queryset(self):
        # Group by week starting date and aggregate hours for each group
        return (
            super().get_queryset()
            .annotate(week=TruncWeek('date'))
            .values('week')
            .annotate(total_hours=Sum('hours'))
            .order_by('-week')
        )

class MonthlyTimesheetManager(models.Manager):
    def get_queryset(self):
        # Group by month and aggregate hours for each group
        return (
            super().get_queryset()
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total_hours=Sum('hours'))
            .order_by('-month')
        )

class DailyTimesheetManager(models.Manager):
    def get_queryset(self):
        # Group by day and aggregate hours for each day
        return (
            super().get_queryset()
            .annotate(day=TruncDay('date'))
            .values('day')
            .annotate(total_hours=Sum('hours'))
            .order_by('-day')
        )

class Timesheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    start_of_week = models.DateField()
    
    objects = models.Manager()  # Default manager
    daily = DailyTimesheetManager()  # Custom manager for daily view
    weekly = WeeklyTimesheetManager()  # Custom manager for weekly view
    monthly = MonthlyTimesheetManager()  # Custom manager for monthly view

    def __str__(self):
        return f'{self.user.username} - {self.project.name} - {self.task.name} - {self.date} - {self.hours} - {self.start_of_week}'

