from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from accountapp.models import Member
from board.models import QABoard


def board_list(request):
    postlist = QABoard.objects.all()
    return render(request, 'board/board_list.html', {'postlist': postlist})
# Create your views here.

def board_write(request):
    if request.method=="POST":
        post_num = len(QABoard.objects.all())
        title = request.POST.get('title')
        content = request.POST.get('content')
        new_list = QABoard(id=post_num+1, user_id=request.session['user_id'], title=title, content=content)
        new_list.save()
        return redirect('/app/board/')
    return render(request, "board/board_write.html")

def board_detail(request, id):
    post = QABoard.objects.get(id=id)
    return render(request, 'board/board_detail.html', {'post': post})

def board_update(request, up_id):
    post_update = QABoard.objects.get(id=up_id)
    if request.method=="POST":
        post_update.title = request.POST.get('title')
        post_update.content = request.POST.get('content')
        post_update.save()
        return redirect('/app/board/')
    else:
        return render(request, 'board/board_update.html', {'post_update': post_update})

def board_delete(request, del_id): 
    post_del = QABoard.objects.get(id=del_id)
    print(post_del)
    post_del.delete()
    messages.info(request, "삭제가 완료되었습니다. ")
    return redirect('/app/board/')

