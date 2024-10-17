import datetime
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class BusinessUnit(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name


class Project(models.Model):
	projectmanager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projectmanager")
	name = models.CharField(max_length=254, primary_key=True)
	description = models.TextField()
	start_date = models.DateField()
	end_date = models.DateField(null=True, blank=True)
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
	businessunit = models.ManyToManyField(BusinessUnit)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	# def get_absolute_url(self):
	# 	return reverse('project:project-detail', kwargs={'pk': self})


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
