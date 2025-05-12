from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Topic, Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 

# Create your views here.
def home(request):
    tasks = Task.objects.all()
    return render(request,"myapp/home.html", {"tasks":tasks})

def loginPage(request):

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
    
    return render(request, "myapp/login_register.html")