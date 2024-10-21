from django.contrib import admin

# Register your models here.
from .models import Project, Task, Timesheet


class TaskInline(admin.TabularInline):
    model = Task
    
    
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    inlines = [
        TaskInline,
    ]


admin.site.register(Project, ProjectAdmin)
    

class TimesheetAdmin(admin.ModelAdmin):
    model = Timesheet


admin.site.register(Timesheet, TimesheetAdmin)