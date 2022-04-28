from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from homeapp.models import QABoard, Member


def board_list(request):
    postlist = QABoard.objects.all()
    return render(request, 'board/board_list.html', {'postlist': postlist})
# Create your views here.

def board_write(request):
    if(request.method == "POST"):
        m = Member(user_id=request.session['user_id'])
        title = request.POST.get('title')
        content = request.POST.get('content')
        new_board = QABoard(
            title = title,
            content = content,
            user_id = request.session['user_id'],
        )
        new_board.save()
        return redirect('/board/')
    return render(request, "board/board_write.html")