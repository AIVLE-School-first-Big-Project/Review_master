from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'homeapp'

urlpatterns = [
    path('home/', views.home, name="home"),
    path('login/',views.login, name="login"),
    path('', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('mypage/', views.mypage, name="mypage"),
    path('user_update/', views.user_update, name="user_update"),
    path('user_delete/', views.user_delete, name="user_delete"),
]