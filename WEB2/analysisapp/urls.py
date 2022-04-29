from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'analysisapp'

urlpatterns = [

    # show -> X?
    # index -> X
    # exa1 -> O -> home

    # path('show/', views.show, name='show'),
    # path('index/', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('result/', views.result, name='result'),





    #path('index/search_main/', views.search_main,name='search_main'),
]
