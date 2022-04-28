from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from analysisapp.models import ArticleCode, ArticleInfo, BuyList, ReviewData, ReviewAnalysis, MemberLog, Member
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home(request):
    if request.method == "POST":
        login_id = request.session['user']

        print(f"현재 로그인한 사람 {login_id}")
        company_name = request.POST.get("company", 0)
        article_name = request.POST.get("article_name", 0)

        # 만약 회사명과 제품명이 아무것도 안들어오고 검색된 경우
        if company_name == "" and article_name == "":

            # user = Member.objects.get(user_id=request.session['user'])

            # user.user_pw = "바꾼거"
            # user.save()
            print("검색 다시 하게 만들어야함")

        # 회사명만 안적고 검색한 경우
        elif request.POST.get("company", 0) == "":
            print("제품명과 비슷한 DB가 있으면 보여준다.")

        # 모두 다 잘들어왔다.
        else:
            print("모두다 잘 들어온경우")
            print(company_name)
            print(article_name)

            # 검색 기록 남기기
            MemberLog(user_id=login_id, search_name=article_name,
                      search_company=company_name).save()
            try:
                article_code = ArticleCode.objects.get(
                    search_name=article_name)
                print(article_code.article_id)
                article_id = article_code.article_id
                review = ReviewData.objects.filter(
                    article_id=article_id)

                for re in review:
                    print(re.content)
            except:
                print("결과가 없습니다.")

    return render(request, 'analysisapp/home.html')


@csrf_exempt
def search(request):
    if request.method == "POST":
        print(request.session["user"])

        company_name = request.POST.get("company", 0)
        article_name = request.POST.get("article_name", 0)

        # 만약 회사명과 제품명이 아무것도 안들어오고 검색된 경우
        if company_name == "" and article_name == "":
            print("검색 다시 하게 만들어야함")

        # 회사명만 안적고 검색한 경우
        elif request.POST.get("company", 0) == "":
            print("제품명과 비슷한 DB가 있으면 보여준다.")

        # 모두 다 잘들어왔다.
        else:
            print("모두다 잘 들어온경우")

    # 예비 로그인 상태로 만들기
    request.session['user'] = 'jang'
    return render(request, 'analysisapp/search.html')


def get_search_name(search_name):
    """
        params:
            search_name : 페이지에서 검색한 이름
        ------------
        return:
            list : 리뷰건수, 리뷰요약, 구매리스트

    """
    # 검색 된 단어가 아티클인포에 있는지 확인

    # 없으면 아티클인포에 해당 단어를 추가 저장 -> 아티클인포에서 아티클코드 + 서치네임 0 0 0

    list = get_object_or_404(
        ArticleInfo, search_name=search_name)  # 리뷰건수, 리뷰요약, 구매리스트
    return list

# 리뷰건수
# 리뷰건수를 반환하는 함수


def review_num(article_code):
    row = ReviewData.objects.filter(article_code=article_code)
    return row


def show(request):
    if request.method == "POST":
        search_name = request.POST.get('search-item')
        time = datetime.now()
    return HttpResponse((search_name, time))
