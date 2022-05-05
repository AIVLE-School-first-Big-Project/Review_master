from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'homeapp'

urlpatterns = [
    path('home/', views.home, name="home"),
    path('', views.home, name="home"),
]