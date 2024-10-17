from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from django.views import View
from .models import Project, Task, BusinessUnit
from .forms import TaskForm, TaskFormSet, ProjectForm


# Create your views here.
class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'  # template for the list view
    context_object_name = 'projects'  # custom name for context

    # def get_context_data(self, **kwargs):
    #     context = super(ProjectListView, self).get_context_data(**kwargs)
    #     context['project_list'] = Project.objects.all()
    #     return context
    

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_form.html'
    success_url = reverse_lazy('project_list')


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_form.html'  # template for the update form
    success_url = reverse_lazy('project_list')  # redirect to list view on success


class TaskListView(View):
    def get(self, request, project_name):
        project = Project.objects.get(name=project_name)
        tasks = project.tasks.all()
        return render(request, 'task_list.html', {'project': project, 'tasks': tasks})

class TaskCreateView(View):
    def get(self, request, project_name):
        project = Project.objects.get(name=project_name)
        formset = TaskFormSet(queryset=Task.objects.none())
        return render(request, 'task_form.html', {'project': project, 'formset': formset})

    def post(self, request, project_name):
        project = Project.objects.get(name=project_name)
        formset = TaskFormSet(request.POST)
        if formset.is_valid():
            tasks = formset.save(commit=False)
            for task in tasks:
                task.project = project  # Associate the task with the project
                task.save()
            return redirect('task_list', project_name=project_name)
        return render(request, 'task_form.html', {'project': project, 'formset': formset})