from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Topic, Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import UserCreationForm
from .forms import TaskForm

# Create your views here.
def home(request):
    tasks = Task.objects.all()
    return render(request,"myapp/home.html", {"tasks":tasks})

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