from datetime import datetime
from django.shortcuts import render
from analysisapp.models import ArticleCode, ArticleInfo, BuyList, ReviewData, ReviewAnalysis, MemberLog, Member
import random
from django.views.decorators.csrf import csrf_exempt
app_name = 'homeapp'


@csrf_exempt
def home(request):
    # login_id = request.session.get('user_id', "nonuser")
    # 추천 검색어 가져오기
    # 랜덤으로 10개 가져온다.

    if request.method == "POST":

        login_id = request.session.get('user_id', "nonuser")

        pay = request.POST.get("pay", 0)

        if pay == "pay_0" and login_id != "nonuser":
            m_member = Member.objects.get(user_id=login_id)
            m_member.user_class = 0
            m_member.save()
        elif pay == "pay_990" and login_id != "nonuser":
            m_member = Member.objects.get(user_id=login_id)
            m_member.user_class = 1
            m_member.save()

    m_article_code = ArticleCode.objects.all()
    recommand_list = {}

    if len(m_article_code) > 10:
        num = random.sample([i for i in range(len(m_article_code))], 10)
        company = []
        name = []
        for i in num:

            company.append(m_article_code[i].search_company)
            name.append(m_article_code[i].search_name)
        recommand_list["company"] = company
        recommand_list["name"] = name

    else:
        num = random.sample(
            [i for i in range(len(m_article_code))], len(m_article_code))
        company = []
        name = []
        for i in num:

            company.append(m_article_code[i].search_company)
            name.append(m_article_code[i].search_name)
        recommand_list["company"] = company
        recommand_list["name"] = name

    check_box = {
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0,
        "sixth": 0,
        "seventh": 0,
        "eighth": 0,
        "ninth": 0,
        "tenth": 0
    }
    count_col = ["first", "second", "third", "fourth", "fifth",
                 "sixth", "seventh", "eighth", "ninth", "tenth"]

    for i in range(len(recommand_list["company"])):

        check_box[count_col[i]] = 1

    # 전체 인기 검색어 진행
    m_hot_keyword = ArticleInfo.objects.order_by('-search_cnt')[:10]
    hot_keyword = []

    for idx, info in enumerate(m_hot_keyword):

        m_article_code = ArticleCode.objects.get(article_id=info.article_id)

        hot_keyword.append([idx+1, m_article_code.search_company,
                           m_article_code.search_name, info.search_cnt])

    # # 연령대별 인기 검색어 가져오기 - 남성 2030
    m_twenty_male = ArticleInfo.objects.order_by('-twenty_male_cnt')[:10]
    twenty_male = []

    for idx, info in enumerate(m_twenty_male):

        m_article_code = ArticleCode.objects.get(article_id=info.article_id)

        twenty_male.append([idx+1, m_article_code.search_company,
                           m_article_code.search_name, info.twenty_male_cnt])

    # # 연령대별 인기 검색어 가져오기 - 여성 2030
    m_twenty_female = ArticleInfo.objects.order_by('-twenty_female_cnt')[:10]
    twenty_female = []

    for idx, info in enumerate(m_twenty_female):

        m_article_code = ArticleCode.objects.get(article_id=info.article_id)

        twenty_female.append([idx+1, m_article_code.search_company,
                              m_article_code.search_name, info.twenty_female_cnt])

    # # 연령대별 인기 검색어 가져오기 - 남성 4050
    m_fourty_male = ArticleInfo.objects.order_by('-fourty_male_cnt')[:10]
    fourty_male = []

    for idx, info in enumerate(m_fourty_male):

        m_article_code = ArticleCode.objects.get(article_id=info.article_id)

        fourty_male.append([idx+1, m_article_code.search_company,
                           m_article_code.search_name, info.fourty_male_cnt])

    # # 연령대별 인기 검색어 가져오기 - 여성 4050
    m_fourty_female = ArticleInfo.objects.order_by('-fourty_female_cnt')[:10]
    fourty_female = []

    for idx, info in enumerate(m_fourty_female):

        m_article_code = ArticleCode.objects.get(article_id=info.article_id)

        fourty_female.append([idx+1, m_article_code.search_company,
                              m_article_code.search_name, info.fourty_female_cnt])

    # member = Member.objects.get(user_id=login_id)
    # age_group = age_group_check(member.user_birth)
    # sex = member.user_sex

    return render(request, "homeapp/contents.html",
                  {
                      "recommand_list": recommand_list,
                      "check_box": check_box,
                      "hot_keyword": hot_keyword,
                      "twenty_male": twenty_male,
                      "twenty_female": twenty_female,
                      "fourty_male": fourty_male,
                      "fourty_female": fourty_female


                  })
