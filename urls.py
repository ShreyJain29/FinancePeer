from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('login', views.loginuser, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logoutuser, name="logout"),
    path("" , views.index , name="index"),
    path("display" , views.display_data , name="display"),

]