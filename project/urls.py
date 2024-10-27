"""
URL configuration for ksheet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from .views import ProjectListView, ProjectUpdateView, ProjectCreateView, timesheet_list_view,  TimesheetView


app_name = 'project'
urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/create/', ProjectCreateView.as_view(), name='project_create'),
    path('projects/update/<int:pk>/', ProjectUpdateView.as_view(), name='project_update'),
    path('timesheet/<str:week_start>/', TimesheetView.as_view(), name='timesheet_view'),
    #path('timesheet/<str:week_start>/', timesheet_detail_view, name='timesheet_detail'), #reverse('timesheet_detail_view', args=[1, str(week_start)])
    path('timesheets/', timesheet_list_view, name='timesheet_list'),
]