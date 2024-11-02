from django.contrib import admin
from django.urls import path
from .views import ProjectListView, ProjectUpdateView, ProjectCreateView, TimesheetView, TimesheetListView, WeeklyTimesheetView
from .views import DailyTimesheetList, WeeklyTimesheetList, MonthlyTimesheetList, MonthlyTimesheetView


app_name = 'project'
urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/create/', ProjectCreateView.as_view(), name='project_create'),
    path('projects/update/<int:pk>/', ProjectUpdateView.as_view(), name='project_update'),    
    #path('timesheet/<str:week_start>/', timesheet_detail_view, name='timesheet_detail'), #reverse('timesheet_detail_view', args=[1, str(week_start)])
    path('timesheets/', TimesheetListView.as_view(), name='timesheet_list'),
    path('timesheets/daily/', DailyTimesheetList.as_view(), name='daily_timesheet_list'),
    path('timesheets/weekly/', WeeklyTimesheetList.as_view(), name='weekly_timesheet_list'),
    path('timesheets/weekly/<int:year>/<int:week>/', WeeklyTimesheetView.as_view(), name='weekly_timesheet'),
    path('timesheets/monthly/', MonthlyTimesheetList.as_view(), name='monthly_timesheet_list'),
    path('timesheets/monthly/<int:year>/<str:month>/', MonthlyTimesheetView.as_view(), name='monthly_timesheet'),
    path('timesheet/<str:week_start>/', TimesheetView.as_view(), name='timesheet_view'),
]