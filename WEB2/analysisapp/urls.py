from django.urls import path
from . import views

app_name = 'analysisapp'

urlpatterns = [
    path('result/', views.result, name='result'),
    path('detail/<int:sentiment_id>', views.detail, name='detail'),
]
