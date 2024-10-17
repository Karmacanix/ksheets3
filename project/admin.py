from django.contrib import admin

# Register your models here.
from project.models import Project, BusinessUnit


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "project_status", "projectmanager",)
  
  
class BusinessUnitAdmin(admin.ModelAdmin):
    list_display = ("name",)
    

admin.site.register(Project, ProjectAdmin)
admin.site.register(BusinessUnit, BusinessUnitAdmin)