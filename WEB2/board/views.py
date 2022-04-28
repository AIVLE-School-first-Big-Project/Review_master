from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from homeapp.models import Member, QABoard


def board_list(request):
    postlist = QABoard.objects.all()
    return render(request, 'board/board_list.html', {'postlist': postlist})
# Create your views here.

def board_write(request):
    if(request.method == "POST"):
        m = QABoard.objects.get(user_id=request.session['user_id'])
        title = request.POST.get('title')
        content = request.POST.get('content')
        # new_list = QABoard(user_id=request.session['user-id'], title=title, content=content, )
        m.title = title
        m.content = content
        m.save()
        return redirect('/board/')
    return render(request, "board/board_write.html")