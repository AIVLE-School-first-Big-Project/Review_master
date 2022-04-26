from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'homeapp'

urlpatterns = [
    path('home/', views.home, name="home"),
    path('login/',views.login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('board/', views.board),
    path('mypage/', views.mypage, name="mypage"),
    path('user_delete/', views.user_delete, name="user_delete"),
    path('user_update/<int:pk>/', views.update, name='user_update'),
]