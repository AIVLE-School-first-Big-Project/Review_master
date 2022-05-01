from datetime import datetime
from django.shortcuts import render
from analysisapp.models import ArticleCode, ArticleInfo, BuyList, ReviewData, ReviewAnalysis, MemberLog, Member
import random
app_name = 'homeapp'


def home(request):
    # login_id = request.session.get('user_id', "nonuser")
    # 추천 검색어 가져오기
    # 랜덤으로 10개 가져온다.

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
        "thrid": 0,
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

    for i in range(len(recommand_list)):
        check_box[count_col[i]] = 1

    # # 연령대별 인기 검색어 가져오기
    # member = Member.objects.get(user_id=login_id)
    # age_group = age_group_check(member.user_birth)
    # sex = member.user_sex
    print(recommand_list)

    return render(request, "homeapp/contents.html",
                  {
                      "recommand_list": recommand_list,
                      "check_box": check_box
                  })
