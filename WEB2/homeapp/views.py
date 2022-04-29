from datetime import datetime
from django.shortcuts import render

app_name = 'homeapp'

def home(request):
    return render(request, "homeapp/contents.html")
