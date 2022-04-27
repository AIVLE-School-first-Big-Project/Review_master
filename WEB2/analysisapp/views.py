from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from analysisapp.models import ArticleInfo, ReviewData, ReviewAnalysis, BuyList
# from analysisapp.models import  BuyList, ReviewData,ReviewAnalysis
# Create your views here.


# def show(request):
#     return render(request, 'analysisapp/show.html')

# 메인페이지
def home(request):

    return render(request, 'analysisapp/home.html')

def serach(request):

    return render(request, 'analysisapp/serach.html')
# #
# def search_main(request):
#     if request.method == "POST":
#         pass
#         # search_name = request.POST.get('search_name')
#         # list = get_object_or_404(ArticleInfo, search_name=request.POST.get('search_name'))
#         # item = get_object_or_404(ReviewAnalysis, article_code=list.article_code)
#         # row = ReviewData.objects.filter(article_code=list.article_code)
#         # item2 = list.article_code
#         # item3=BuyList.objects.filter(article_code=list.article_code).order_by('buy_coin')
#         # return render(request, 'analysisapp/index.html', {'item': item,'item2':item2,'row':row,'item3':item3,'list':list})

#     return HttpResponseRedirect('/analysis/show/')

# # def index(request):
# #     if request.method == "GET":
# #         print("get")
# #         pass
# #     elif request.method == "POST":
# #         article_code= 1

# #         #검색된 게시물 이름
# #         search_name=2

# #         # 리뷰 게시물 개수
# #         article_review_cnt= 3

# #         #순수 리뷰 게시물 개수
# #         article_pure_review_cnt= 4

# #         #검색 카운트
# #         search_cnt= 5

# #         m = ArticleInfo(
# #             article_code = article_code,
# #             search_name= search_name,
# #             article_review_cnt=article_review_cnt,
# #             article_pure_review_cnt=article_pure_review_cnt,
# #             search_cnt=search_cnt
# #         )
# #         m.save()
# #         print("Post")
# #     return HttpResponseRedirect('/analysis/show')

# def index(request):
#     print("아무나1")
#     if request.method == "GET":
#         article_code = request.GET.get('article_code',False)
#         print("아무나2")
#         if article_code:
#             row = ReviewData.objects.filter(article_code=article_code)
#             # for data in row:
#             # blog_code= row.blog_code
#             # print('ddddddd',blog_code)
#             # item = get_object_or_404(ReviewAnalysis, blog_code=blog_code)

#             # list = get_object_or_404(ArticleInfo, article_code=article_code)
#             #item3=BuyList.objects.filter(article_code=article_code).order_by('buy_coin')
#             return render(request, 'analysisapp/index.html', {'row':row})
#             #return render(request, 'analysisapp/index.html', {'item': item,'item2':article_code,'row':row})
#         else :
#             print("아무나3")
#             return HttpResponseRedirect('/app/home')
#     elif request.method == "POST":
#         search_name = request.POST.get('search_name',False)
#         print("아무나4")
#         if search_name:
#             # list = get_object_or_404(ArticleInfo, search_name=search_name) #리뷰건수, 리뷰요약, 구매리스트
#             list = get_search_name(search_name)
#             #row = ReviewData.objects.filter(article_code=list.article_code) #리뷰건수
#             row = review_num(list.article_code)
#             # rd=get_object_or_404(ReviewData,article_code=list.article_code) #리뷰요약
#             # ra=get_object_or_404(ReviewAnalysis, blog_code=rd.blog_code)#리뷰요약, 연관어

#             # rd=ReviewData.objects.get(article_code=list.article_code) #리뷰요약
#             # ra=ReviewAnalysis.objects.get(blog_code=rd.blog_code)#리뷰요약, 연관어
#             rd=ReviewData.objects.filter(article_code=list.article_code) #리뷰요약
#             # rd.first() #리뷰요약
#             #for r in rd:
#             # 가격 3000원
#             #ra=ReviewAnalysis.objects.get(blog_code=r.blog_code)#리뷰요약, 연관어
#             # item = get_object_or_404(ReviewAnalysis, blog_code=a.blog_code)
#             # item2 = list.article_code
#             item3=BuyList.objects.filter(article_code=list.article_code).order_by('price')#구매리스트
#             return render(request, 'analysisapp/index.html', {'row':row,'list':list,'ra':ra,'item3':item3})
#         else :
#             return render(request, 'analysisapp/show.html')
#     print("아무나")
#     return HttpResponseRedirect('app/analysis/show')

# list : return 값, 리뷰건수, 리뷰요약, 구매리스트
# searname를 post로 받았을 때 ArticleInfo에서 article_code를 얻기 위해 하는 함수


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
