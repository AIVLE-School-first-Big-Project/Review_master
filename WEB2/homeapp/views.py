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
    recommand_list = []

    if len(m_article_code) > 10:
        num = random.sample([i for i in range(len(m_article_code))], 10)

        for i in num:
            recommand_list.append(
                m_article_code[i].search_company + " " + m_article_code[i].search_name)

    else:
        num = random.sample(
            [i for i in range(len(m_article_code))], len(m_article_code))

        for i in num:
            recommand_list.append(
                m_article_code[i].search_company + " " + m_article_code[i].search_name)
    # # 연령대별 인기 검색어 가져오기
    # member = Member.objects.get(user_id=login_id)
    # age_group = age_group_check(member.user_birth)
    # sex = member.user_sex

    return render(request, "homeapp/contents.html",
                  {
                      "recommand_list": recommand_list
                  })
