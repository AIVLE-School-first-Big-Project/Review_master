from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.board_list, name="board_list"),
    path('write/', views.board_write, name="write"),
    path('detail/<int:id>/', views.board_detail, name="detail"),
    path('', views.board_delete, name="delete"),
]