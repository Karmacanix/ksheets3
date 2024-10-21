import datetime
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
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
    

class Timesheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.user.username} - {self.project.name} - {self.task.name} - {self.date} - {self.hours}'

