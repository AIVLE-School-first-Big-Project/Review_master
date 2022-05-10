from django.shortcuts import render
from django.shortcuts import redirect
from board.models import QABoard
from analysisapp.models import MemberLog

from accountapp.models import Member
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

import bcrypt

app_name = 'accountapp'


def board(request):
    return render(request, "accountapp/board.html")


def login(request):
    if request.method == "POST":
        user_id = request.POST.get('username')
        user_pw = request.POST.get('password')
        try:
            m = Member.objects.get(user_id=user_id)

            if not bcrypt.checkpw(user_pw.encode('utf-8'),
                                  m.user_pw.encode('utf-8')):
                m = ""

        except Exception:
            m = ""
            messages.warning(request, '잘못 입력하셨거나 존재하지 않는 사용자 정보입니다.')

        if m != "":
            request.session['user_id'] = m.user_id
            request.session['user_nickname'] = m.user_nickname
            request.session['user_class'] = m.user_class
            return redirect('/app/home')
        else:
            return render(request,
                          'accountapp/login.html',
                          {'error': 'username or password is incorrect'})
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
            Member.objects.get(user_id=user_id)

            messages.info(request, '사용중인 아이디입니다.')
            return HttpResponseRedirect(reverse('accountapp:signup'))
        except Member.DoesNotExist:

            hased_pw = bcrypt.hashpw(user_pw.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hased_pw.decode('utf-8')

            m = Member(user_id=user_id,
                       user_pw=decoded_hashed_pw,
                       user_nickname=user_nickname,
                       user_email=user_email,
                       user_class=user_class,
                       user_sex=user_sex,
                       user_status=user_status,
                       user_birth=user_birth)
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

            hased_pw = bcrypt.hashpw(user_pw.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hased_pw.decode('utf-8')

            m.user_pw = decoded_hashed_pw
            m.user_email = user_email
            m.user_nickname = user_nickname
            m.user_sex = user_sex
            m.user_birth = user_birth
            m.update_time = datetime.now().strftime('%Y-%m-%d')
            m.save()

            request.session['user_nickname'] = user_nickname

            return redirect('/app/account/mypage')
    return render(request, 'accountapp/user_update.html')


def user_delete(request):
    if request.method == 'POST':
        m_qaboard = QABoard.objects.filter(user_id=request.session['user_id'])
        m_qaboard.delete()

        m_member_log = MemberLog.objects.\
            filter(user_id=request.session['user_id'])
        m_member_log.delete()

        m_member = Member.objects.get(user_id=request.session['user_id'])
        m_member.delete()

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


def agreement(request):
    if request.method == "POST":
        if request.POST.get('agreement', False):
            request.session['agreement'] = True
            return redirect('/app/account/signup')
        else:
            messages.info(request, "약관에 동의해주세요.")
            return render(request, 'accountapp/agreement.html')
    else:
        request.session['agreement'] = False
        return render(request, 'accountapp/agreement.html')
