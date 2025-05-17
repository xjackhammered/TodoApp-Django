from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Topic, Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import UserCreationForm
from .forms import TaskForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="login")
def home(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ""
    tasks = Task.objects.filter(
        Q(topic__name__icontains=q),
        host = request.user
    )

    topics = Topic.objects.all()
    return render(request,"myapp/home.html", {"tasks":tasks, "topics":topics})

def loginPage(request):

    page = "login"

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'Username or password does not exist.')
    
    return render(request, "myapp/login_register.html", {"page":page})

def logoutUser(request):
    logout(request)
    return redirect("home")

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error has occured during registration.")
    return render(request, "myapp/login_register.html", {"form":form})

@login_required(login_url="login")
def addTask(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.host = request.user
            task.save()
            return redirect("home")
    
    return render(request, "myapp/task_form.html", {"form":form})

@login_required(login_url="login")
def updateTask(request, id):
    task = Task.objects.get(id=id)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("home")
    
    return render(request,'myapp/task_form.html',{"form":form})

@login_required(login_url="login")
def deleteTask(request, id):
    task = Task.objects.get(id=id)
    if request.method == "POST":
        task.delete()
        return redirect("home")
    return render(request, "myapp/delete.html", {'obj':task})
