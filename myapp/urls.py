from django.urls import path   
from .import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path("login/", views.loginPage, name="login"),
    path("logout/",views.logoutUser, name="logout"),
    path("register/",views.registerUser, name="register"),
    path("add-task/", views.addTask, name="add-task"),
    path("update-task/<int:id>/", views.updateTask, name="update-task"),
]