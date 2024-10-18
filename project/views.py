from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from django.views import View
from .models import Project, Task
from .forms import TaskForm, TaskFormSet, ProjectForm


# Create your views here.
class ProjectListView(ListView):
    model = Project
    template_name = 'project/project_list.html'  
    

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_form.html'
    success_url = reverse_lazy('project_list')


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_form.html'  
    success_url = reverse_lazy('project_list') 


class TaskListView(View):
    model = Task
    template_name = 'project/task_list.html'
    
    
    def get(self, request, project):
        project = Project.objects.get(id=project_id)
        tasks = Task.objects.filter(project=project_id)
        return render(request, 'project/task_list.html', {'project': project, 'tasks': tasks})


class TaskCreateView(View):
    model = Task
    form_class = TaskForm
    template_name = 'project/task_form.html'
    success_url = reverse_lazy('task_list')
    
    def get(self, request, project):
        project = Project.objects.get(id=project_id)
        formset = TaskFormSet(queryset=Task.objects.none())
        return render(request, 'project/task_form.html', {'project': project, 'formset': formset})

    def post(self, request, project):
        project = Project.objects.get(id=project_id)
        formset = TaskFormSet(request.POST)
        if formset.is_valid():
            tasks = formset.save(commit=False)
            for task in tasks:
                task.project = project_id  # Associate the task with the project
                task.save()
            return redirect('project/task_list', project_id=project_id)
        return render(request, 'project/task_form.html', {'project': project, 'formset': formset})