from django.urls import path
from . import views


app_name = 'board'

urlpatterns = [
    path('', views.board_list, name="board_list"),
    path('write/', views.board_write, name="write"),
    path('detail/<int:id>/', views.board_detail, name="detail"),
    path('<int:del_id>/', views.board_delete, name="delete"),
    path('update/<int:up_id>/', views.board_update, name="update"),
    path('<int:post_id>', views.file_download, name="download"),
]
