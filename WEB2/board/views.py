import mimetypes
from wsgiref.util import FileWrapper
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from accountapp.models import Member
from board.models import QABoard
from django.db.models import Max
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
import os

def board_list(request):
    postlist = QABoard.objects.all()
    return render(request, 'board/board_list.html', {'postlist': postlist})
# Create your views here.


def board_write(request):
    if request.method == "POST":
        # 관리자가 답글을 다는 경우
        if request.session['user_class'] == 99:
            post_id = request.POST.get('question_id')
            new_answer = QABoard.objects.get(id=post_id)

            answer_title = request.POST.get('answer_title')
            answer_content = request.POST.get('answer_content')

            new_answer.answer_title = answer_title
            new_answer.answer_content = answer_content
            new_answer.save()
            return redirect('/app/board/')

        # 사용자가 질문글을 작성하는 경우
        else:
            m_QABoard = QABoard()
            m_QABoard.user_id = request.session["user_id"]
            m_QABoard.title = request.POST.get("title")
            m_QABoard.content = request.POST.get('content')
            m_QABoard.file_name = request.FILES.get('file_name')
            m_QABoard.save()

            return redirect('/app/board/')

    return render(request, "board/board_write.html")


def board_detail(request, id):
    post = QABoard.objects.get(id=id)
    return render(request, 'board/board_detail.html', {'post': post})


def board_update(request, up_id):
    post_update = QABoard.objects.get(id=up_id)
    if request.method == "POST":
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

from wsgiref.util import FileWrapper
def file_download(request, post_id):
    file = QABoard.objects.get(id=post_id)
    file_path = file.file_name.path

    file_mimetype = mimetypes.guess_type(file_path)
    # fs = FileSystemStorage(file_path)
    
    response = FileResponse(open(file_path, 'rb'), content_type=file_mimetype)
    # response = HttpResponse(file_wrapper, content_type=file_mimetype)
    response['X-Sendfile'] = file_path
    # response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment;filename=%s' % str(file_path) 
    return response


