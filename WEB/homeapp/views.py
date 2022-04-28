from django.shortcuts import render

# Create your views here.
from curses import raw
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from homeapp.models import Member
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

app_name = 'homeapp'

def home(request):
    return render(request, 'homeapp/home.html')

def board(request):
    return render(request, "homeapp/board.html")

def login(request):
    if request.method == "POST":
        user_id = request.POST.get('username')
        user_pw = request.POST.get('password')
        try:
            m = Member.objects.get(user_id = user_id, user_pw = user_pw)
        except:
            m = ""
            messages.warning(request, '잘못 입력하셨거나 존재하지 않는 사용자 정보입니다.')
        if m!="":
            request.session['user_id'] = m.user_id
            request.session['user_nickname'] = m.user_nickname
            request.session['user_email'] = m.user_email
            return redirect('/app/home')
        else:
            return render(request, 'homeapp/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'homeapp/login.html')
    
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
        user_pw =  request.POST.get('password1')
        user_pw_check =request.POST.get('password2')
        user_email = request.POST.get('email')
        user_nickname = request.POST.get('nickname')
        user_class = request.POST.get('user_class')
        user_birth = request.POST.get('user_birth')
        user_sex = request.POST.get('user_sex')
        user_status = request.POST.get('user_status')

        if user_pw_check != user_pw:
            messages.info(request, '비밀번호가 일치하지 않습니다.')
            return HttpResponseRedirect(reverse('homeapp:signup'))   
        try:
            user = Member.objects.get(user_id = user_id)

            messages.info(request, '사용중인 아이디입니다.')
            return HttpResponseRedirect(reverse('homeapp:signup'))   
        except Member.DoesNotExist as e:
            m = Member(user_id=user_id, user_pw=user_pw, user_nickname=user_nickname, user_email=user_email,user_class=user_class,user_sex=user_sex, user_status=user_status, user_birth=user_birth)
            m.save()
            return HttpResponseRedirect(reverse('homeapp:login'))   
    else:
        return render(request,'homeapp/signup.html')  

def mypage(request):
    return render(request, 'homeapp/mypage.html')

def user_update(request):
    if request.method == "GET":
        return render(request, 'homeapp/user_update.html')
    
    elif request.method == "POST":
        m = Member.objects.get(user_id=request.session['user_id'])

        user_pw =  request.POST.get('password1')
        user_pw_check =request.POST.get('password2')
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
            return redirect('/app/mypage')
    return render(request, 'homeapp/user_update.html')

def user_delete(request):
    if request.method == 'POST':
        m = Member(user_id=request.session['user_id'])
        m.delete()
        logout(request)
        return redirect('homeapp:home')
    return render(request, 'homeapp/user_delete.html')