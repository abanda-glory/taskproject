from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

class TaskForm(forms.ModelForm):
    class Meta: #Meta class is used for configurations
        model = Task
        fields = ['title', 'description', 'completed'] #form fields
        
#Home view
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            #create task but dont upload to database
            task = form.save(commit=False)
            #Assign task to current user
            task.user = request.user
            #Now save to database because commit is set to false
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST,  instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    return redirect('task_list')

#Register User
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

#User Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm
    return render(request, 'tasks/login.html', {'form': form})

#User logout
def user_logout(request):
    logout(request)
    return redirect('login')

# Create your views here.
