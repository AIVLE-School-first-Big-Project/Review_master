from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accountapp'

urlpatterns = [
    path('AAAA/', views.test1, name='AAAA'),
    path('login/',views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    # path('board/', views.board),
    path('mypage/', views.mypage, name="mypage"),
    path('user_update/', views.user_update, name="user_update"),
    path('user_delete/', views.user_delete, name="user_delete"),
    path('user_qna/', views.user_qna, name="user_qna"),
    path('user_log/', views.user_log, name="user_log"),
]