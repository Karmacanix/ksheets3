from django.contrib import admin

# Register your models here.
from project.models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project_status", "projectmanager",)
 

admin.site.register(Project, ProjectAdmin)