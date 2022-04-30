from datetime import datetime
from django.shortcuts import render

# Create your views here.
from curses import raw
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from board.models import QABoard
from analysisapp.models import MemberLog

from accountapp.models import Member
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# from argon2 import PasswordHasher

app_name = 'accountapp'


def test1(request):
    print("접속?")
    return render(request, "accountapp/test.html")
    # return HttpResponseRedirect(reverse('homeapp:home'))


def board(request):
    return render(request, "accountapp/board.html")


def login(request):
    if request.method == "POST":
        user_id = request.POST.get('username')
        user_pw = request.POST.get('password')
        try:
            m = Member.objects.get(user_id=user_id, user_pw=user_pw)
        except:
            m = ""
            messages.warning(request, '잘못 입력하셨거나 존재하지 않는 사용자 정보입니다.')
        if m != "":
            request.session['user_id'] = m.user_id
            request.session['user_nickname'] = m.user_nickname
            request.session['user_class'] = m.user_class
            return redirect('/app/home')
        else:
            return render(request, 'accountapp/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'accountapp/login.html')


def logout(request):
    try:
        del request.session['user_id']
        del request.session['user_nickname']
    except KeyError:
        pass
    return redirect('/app/home')


def signup(request):
    if request.method == 'POST':

        user_id = request.POST.get('username')
        user_pw = request.POST.get('password1')
        user_pw_check = request.POST.get('password2')
        user_email = request.POST.get('email')
        user_nickname = request.POST.get('nickname')
        user_class = request.POST.get('user_class')
        user_birth = request.POST.get('user_birth')
        user_sex = request.POST.get('user_sex')
        user_status = request.POST.get('user_status')

        if user_pw_check != user_pw:
            messages.info(request, '비밀번호가 일치하지 않습니다.')
            return HttpResponseRedirect(reverse('accountapp:signup'))
        try:
            user = Member.objects.get(user_id=user_id)

            messages.info(request, '사용중인 아이디입니다.')
            return HttpResponseRedirect(reverse('accountapp:signup'))
        except Member.DoesNotExist as e:
            m = Member(user_id=user_id, user_pw=user_pw, user_nickname=user_nickname, user_email=user_email,
                       user_class=user_class, user_sex=user_sex, user_status=user_status, user_birth=user_birth)
            m.save()
            return HttpResponseRedirect(reverse('accountapp:login'))
    else:
        return render(request, 'accountapp/signup.html')


def mypage(request):
    return render(request, 'accountapp/mypage.html')


def user_update(request):
    if request.method == "GET":
        m = Member.objects.get(user_id=request.session['user_id'])
        return render(request, 'accountapp/user_update.html', {'m': m})

    elif request.method == "POST":
        m = Member.objects.get(user_id=request.session['user_id'])
        user_pw = request.POST.get('password1')
        user_pw_check = request.POST.get('password2')
        user_email = request.POST.get('email')
        user_nickname = request.POST.get('nickname')
        user_sex = request.POST.get('user_sex')
        user_birth = request.POST.get('user_birth')

        if user_pw != user_pw_check:
            messages.warning(request, '비밀번호가 일치하지 않습니다. 다시 시도하세요!')
        else:
            m.user_pw = user_pw
            m.user_email = user_email
            m.user_nickname = user_nickname
            m.user_sex = user_sex
            m.user_birth = user_birth
            m.update_time = datetime.now().strftime('%Y-%m-%d')
            m.save()
            return redirect('/app/account/mypage')
    return render(request, 'accountapp/user_update.html')


def user_delete(request):
    if request.method == 'POST':
        b = QABoard.objects.filter(user_id=request.session['user_id'])
        b.delete()

        l = MemberLog.objects.filter(user_id=request.session['user_id'])
        l.delete()

        m = Member.objects.get(user_id=request.session['user_id'])
        m.delete()

        logout(request)
        return redirect('/app/home')
    return render(request, 'accountapp/user_delete.html')


def user_qna(request):
    postlist = QABoard.objects.filter(user_id=request.session['user_id'])
    return render(request, 'accountapp/user_qna.html', {'postlist': postlist})


def user_log(request):
    logs = MemberLog.objects.filter(user_id=request.session['user_id'])
    return render(request, 'accountapp/user_log.html', {'logs': logs})


def pay(request):
    return render(request, 'accountapp/pay.html')
