from datetime import datetime
from django.shortcuts import render

# Create your views here.
from curses import raw
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from accountapp.models import Member
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

app_name = 'accountapp'


def test1(request):
    print("접속?")
    return render(request, "accountapp/test.html")
    # return HttpResponseRedirect(reverse('homeapp:home'))


def login(request):
    if request.method == "POST": 
        user_id = request.POST.get('username')
        user_pw = request.POST.get('password')
        try:
            m = Member.objects.get(user_id = user_id, user_pw = user_pw)
        except:
            m = ""
        if len(m) !=0:
            request.session['success'] = True
            # return render(request, 'homeapp/home.html')
            return HttpResponseRedirect(reverse('homeapp:home'))  
        else:
            return render(request, 'accountapp/login.html')
    
    return render(request, "accountapp/login.html")

        # 키(key)가 없을 경우, 기본값(예: '0')을 설정하고 세션 값을 가져오기 
        # count = request.session.get('count', '0') 

        # # 세션 값 설정하기 
        # request.session['count'] = '1' 

        # 세션 값 삭제하기 
        # del request.session['count']
        # return redirect('homeapp:home')
        # return render(request, 'homeapp/login.html')
    # else:


def signup(request):
    if request.method == 'POST':

        user_id = request.POST.get('username')
        user_pw =  request.POST.get('password1')
        user_pw_check =request.POST.get('password2')
        user_email = request.POST.get('email')
        user_nickname = request.POST.get('nickname')
        user_class = request.POST.get('user_class')

        if user_pw_check != user_pw:
            messages.info(request, '비밀번호가 일치하지 않습니다.')
            return HttpResponseRedirect(reverse('accountapp:signup'))   
        try:
            user = Member.objects.get(user_id = user_id)

            messages.info(request, '사용중인 아이디입니다.')
            return HttpResponseRedirect(reverse('accountapp:signup'))   
        except Member.DoesNotExist as e:
            m = Member(user_id=user_id, user_pw=user_pw, user_nickname=user_nickname,user_email=user_email,user_class=user_class)
            m.save()
            return HttpResponseRedirect(reverse('accountapp:login'))   
    else:
        return render(request,'accountapp/signup.html')  

def test(request):
    if request.method == "POST":
        search_name = request.POST.get('search_name')
        time = datetime.now()
        return HttpResponse((search_name, time))


def mypage(request):
    if request.method == "POST":
        userclass = request.POST.get('userclass')
        return HttpResponse(userclass)
    return render(request, 'accountapp/mypage.html')

# @login_message_required
def user_delete(request):
    request.user.delete()
    logout(request)
    context = {}
    return render(request, 'accountapp/user_delete.html', context)

def update(request, pk):
    if request.method == "POST":
        form = UserChange(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserChange(instance=request.user)
        context = {
            'form': form
        }
        return render(request, 'accountapp/user_update.html', context)

# class update(UpdateView):
#     model = Member
#     form_class = update
#     success_url = reverse_lazy('homeapp:user_update.html')
def pay(request):
     return render(request, 'accountapp/pay.html')