import secret_key as sk
from django.db import connections
from datetime import datetime
from urllib import response
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from analysisapp.models import ArticleCode, ArticleInfo, BuyList, ReviewData, ReviewAnalysis, MemberLog, Member
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .crawling import crawling_function
from django.urls import reverse
import pandas as pd
import requests
import os
import sys
import json
from datetime import date
from dateutil.relativedelta import relativedelta
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


con = sk.config()
Backend_filtering = "http://" + \
    con.get_secret("HOST") + ":" + con.get_secret("API_PORT") + "/filtering/"
Backend_summary = "http://" + \
    con.get_secret("HOST") + ":" + con.get_secret("API_PORT") + "/summary/"


def age_group_check(birth_date):

    age = relativedelta(
        date.today(), datetime.strptime(str(birth_date), "%Y-%m-%d"))

    if age.years < 40:
        return 0
    else:
        return 1


@csrf_exempt
def result(request):
    if request.method == "POST":
        crawling_check = False
        login_id = request.session.get('user_id', "nonuser")

        print(f"현재 로그인한 사람 {login_id}")

        # 사용자가 검색한 경우
        search_company = request.POST.get("company", 0)
        search_name = request.POST.get("article_name", 0)

        # 검색 결과 로그 출력
        print(search_company)
        print(search_name)

        # 만약 회사명과 제품명이 아무것도 안들어오고 검색된 경우
        if search_company == "" and search_name == "":
            print("검색 다시 하게 만들어야함")

        # 회사명만 안적고 검색한 경우
        elif search_company == "" or search_name == "":
            print("제품명과 비슷한 DB가 있으면 보여준다.")

        # 모두 다 잘들어왔다.   -> 시작.
        else:
            print("모두다 잘 들어온경우")

            MemberLog(user_id=login_id, search_name=search_name,
                      search_company=search_company).save()

            # Article Code에 있는 데이터인지 확인을 하자. + 추가
            m_article_info = ArticleCode.objects.filter(
                Q(search_company=search_company) & Q(search_name=search_name))

            # 0인 경우 : 처음 검색된 경우이다. 이 경우는 크롤링을 진행해주어야 한다.
            if len(m_article_info) == 0:

                crawling_check = True

                # 데이터 코드를 저장시켜준다.
                m_article_code = ArticleCode()
                m_article_code.search_company = search_company
                m_article_code.search_name = search_name

                m_article_code.save()

                # primary key를 받아올 때 회사명과 제품명이 함께 되어있는 경우를 찾는다.
                m_article_info = ArticleCode.objects.filter(
                    Q(search_company=search_company) & Q(search_name=search_name))

            # 제품명과 회사명이 같은 경우 무조건 한가지의 값이 나오므로 첫번째 값의 id를 받아오면 된다.
            article_id = m_article_info[0].article_id   # article_id : 상품 아이디

            # ArticleInfo에서 id와 search_cnt를 1 증가시켜주자. article reviewcnt도 가져올 수 있으니 해당 자료도 가져다 주자.

            # crawling check가 True이면 이전에 없던 데이터였으므로 info안에도 추가시켜주어야한다.
            m_article_info = ArticleInfo.objects.filter(article_id=article_id)
            if len(m_article_info) == 0:
                print("해당 코드가 아직 저장이 안되어있음")
                m_article_info = ArticleInfo()
                m_article_info.article_id = article_id
                m_article_info.search_cnt = 0
                m_article_info.img_url = crawling_function.service_img(
                    search_company, search_name)
                m_article_info.twenty_male_cnt = 0
                m_article_info.twenty_female_cnt = 0
                m_article_info.fourty_male_cnt = 0
                m_article_info.fourty_female_cnt = 0
                m_article_info.save()

            m_member = Member.objects.get(user_id=login_id)
            age_group = age_group_check(m_member.user_birth)
            sex = m_member.user_sex

            m_article_info = ArticleInfo.objects.get(article_id=article_id)
            if sex == 0 or sex == 2:
                if age_group == 0:
                    m_article_info.twenty_female_cnt += 1
                elif age_group == 1:
                    m_article_info.fourty_female_cnt += 1

            if sex == 1 or sex == 2:
                if age_group == 0:
                    m_article_info.twenty_male_cnt += 1
                elif age_group == 1:
                    m_article_info.fourty_male_cnt += 1

            m_article_info.search_cnt += 1
            m_article_info.save()

            # 크롤링 진행 혹은 리뷰 데이터 가져오기
            # 리뷰 테이블에서 데이터 가져오기.
            review = ReviewData.objects.filter(article_id=article_id)
            review_cnt = len(review)
            # 데이터가 하나도 없는 경우 이거나 위에서 크롤링해야한다고 한 경우 크롤링을 진행한다.
            if len(review) == 0 or crawling_check:
                df = crawling_function.service_start(
                    search_company, search_name)
                # df
                # Review Data에 데이터를 추가시켜주자. writer, content, description, content_date, first_img_url, last_img_url, url을 넣어준다.
                url, title, post_date, description, writer, content, first_img_url, last_img_url \
                    = df["url"], df["title"], df["post_date"], df["description"], df["writer"], df["content"], df["first_img"], df["last_img"]

                content_cnt, content_line, quote_cnt, img_cnt, coupang, ndns, dj, sj, bg, dot, bb, z, zzz, zzzz \
                    = df["content_cnt"], df["content_line"], df["quote_cnt"], df["img_cnt"], df["coupa.ng 키워드"], df["내돈내산 키워드"], df["단점 빈도 수"], \
                    df["솔직 빈도 수"],  df["비교 빈도 수"], df["... 빈도 수"], df["ㅠㅠ 빈도 수"], df["ㅋ 빈도 수"], df["ㅋㅋㅋ 빈도 수"], df["ㅋㅋㅋㅋ 빈도 수"]
                # blog_cnt = len(df)
                review_cnt = df.shape[0]

                # 리뷰 데이터가 얼마나 있는지 확인하고 저장
                m_article_info = ArticleInfo.objects.get(article_id=article_id)
                m_article_info.article_review_cnt = review_cnt
                m_article_info.save()
                for idx, i in enumerate(range(len(df))):
                    m_review_data = ReviewData()
                    m_review_data.article_id = article_id
                    m_review_data.writer = writer[i]
                    m_review_data.content = content[i]
                    m_review_data.content_date = post_date[i]
                    m_review_data.first_img_url = first_img_url[i]
                    m_review_data.last_img = last_img_url[i]
                    m_review_data.title = title[i]
                    m_review_data.url = url[i]
                    m_review_data.description = description[i]

                    # 광고 필터링 API 보내기.
                    """"
                        1. 글 데이터 특징 추출
                        2. 이미지 데이터 특징 추출
                    """
                    # 보낼 데이터 양식
                    # 51 -> pro
                    # 1 -> pred

                    data = {
                        "last_img": [str(last_img_url[i])],
                        "content": [str(content[i])],
                        "content_cnt": [int(content_cnt[i])],
                        "content_line": [int(content_line[i])],
                        "내돈내산 키워드": [int(ndns[i])],
                        "img_cnt": [int(img_cnt[i])],
                        "quote_cnt": [int(quote_cnt[i])],
                        "ㅋㅋㅋㅋ 빈도 수": [int(zzzz[i])],
                        "... 빈도 수": [int(dot[i])],
                        "coupan.ng 키워드": [int(coupang[i])],
                        "단점 빈도 수": [int(dj[i])],
                        "솔직 빈도 수": [int(sj[i])],
                        "비교 빈도 수": [int(bg[i])],
                        "ㅋ 빈도 수": [int(z[i])],
                        "ㅠㅠ 빈도 수": [int(bb[i])],
                        "ㅋㅋㅋ 빈도 수": [int(zzz[i])]
                    }

                    print(f"{idx} / {len(df)} 필터링 시작합니다.")
                    response = requests.post(Backend_filtering, json=data)
                    if response.status_code == 200:
                        filter_data = response.json()["pred"]
                        filter_percent = response.json()["pro"]
                    m_review_data.advertise = int(filter_data)
                    m_review_data.advertise_percent = float(
                        filter_percent)  # 확률 처리
                    m_review_data.save()

            # buylist 추가하기
            m_buy_list = BuyList.objects.filter(article_id=article_id)

            if len(m_buy_list) == 0:  # 아무것도 없는 경우
                title, url, image_url, price, mall_name = crawling_function.service_buy(
                    search_company, search_name)

                # 만약 가격차이가 너무 나는 경우는 원하는 값이 아닐수도 있다.

                average_price = sum(price) / len(price)

                for i in range(len(title)):

                    if average_price * 0.7 <= price[i] <= average_price * 1.3:
                        m_buy_list = BuyList()
                        m_buy_list.article_id = article_id
                        m_buy_list.url = url[i]
                        m_buy_list.title = title[i]
                        m_buy_list.price = price[i]
                        m_buy_list.mall_name = mall_name[i]
                        m_buy_list.image_url = image_url[i]
                        m_buy_list.save()

            m_review_analysis = ReviewAnalysis.objects.filter(
                article_id=article_id)
            if len(m_review_analysis) == 0:
                # 분석 api로 데이터 보내기
                """"
                    1. 요약 기능 
                    2. 연관어 분석 기능
                    3. 감성어 분석 기능
                    4. 빈도 수 분석 및 트랜드 분석
                """
                # 보낼 데이터 양식
                item2 = {
                    'artice_code': article_id
                }
                response = requests.post(Backend_summary, params=item2)
                if response.status_code == 200:
                    print("요약 결과")
                    summary_data = response.json()["Decs"]
                    print(summary_data)

            # if len(m_review_analysis) == 0:
                # api로 데이터 보내기

                # 여기는 더미값 넣는 값이다.
                m_review_analysis = ReviewAnalysis()
                m_review_analysis.article_id = article_id
                m_review_analysis.summary = summary_data
                m_review_analysis.emotion_url = "https://t1.daumcdn.net/cfile/tistory/99C9FA335DC91AB810"
                m_review_analysis.associate_url = "https://some.co.kr/renewal_resources/images/association_guide_img.png"
                m_review_analysis.save()

            # reuslt값에 모든 데이터 작성해서 보내주기

            m_article_info = ArticleInfo.objects.get(article_id=article_id)

            data_info = {}
            data_info["company"] = search_company
            data_info["name"] = search_name
            data_info["review_cnt"] = m_article_info.article_review_cnt
            data_info["img_url"] = m_article_info.img_url

            review_list = []
            m_review_data = ReviewData.objects.filter(
                article_id=article_id).order_by("-advertise_percent")

            for review in m_review_data:
                review_dict = {
                    "writer": [],
                    "content": [],
                    "content_date": [],
                    "first_img_url": [],
                    "last_img": [],
                    "url": [],
                    "description": [],
                    "advertise": [],
                    "title": [],
                    "advertise_percent": []
                }

                review_dict["writer"] = review.writer
                review_dict["content"] = review.content
                review_dict["content_date"] = review.content_date
                review_dict["first_img_url"] = review.first_img_url
                review_dict["last_img"] = review.last_img
                review_dict["url"] = review.url
                review_dict["description"] = review.description
                review_dict["advertise"] = review.advertise
                review_dict["title"] = review.title
                review_dict["advertise_percent"] = float(
                    review.advertise_percent) * 100
                review_cnt -= review.advertise
                if review.advertise_percent <= 0.9:
                    continue
                review_list.append(review_dict)

            data_info["pure_cnt"] = review_cnt

            analysis_list = {}
            m_review_analysis = ReviewAnalysis.objects.get(
                article_id=article_id)

            analysis_list["summary"] = m_review_analysis.summary
            analysis_list["emotion_url"] = m_review_analysis.emotion_url
            analysis_list["associate_url"] = m_review_analysis.associate_url

            buy_list = []
            m_buy_list = BuyList.objects.filter(
                article_id=article_id).order_by("price")

            for b in m_buy_list:
                m_buy_dict = {
                    "url": [],
                    "title": [],
                    "price": [],
                    "mall_name": [],
                    "image_url": [],
                }
                m_buy_dict["url"] = b.url
                m_buy_dict["title"] = b.title
                m_buy_dict["price"] = b.price
                m_buy_dict["mall_name"] = b.mall_name
                m_buy_dict["image_url"] = b.image_url
                buy_list.append(m_buy_dict)
            # print(review_list)
            return render(request, 'analysisapp/result.html', {
                "select_num": 1,
                "data_info": data_info,
                "review_list": review_list,
                "analysis_list": analysis_list,
                "buy_list": buy_list
            })

    return HttpResponseRedirect(reverse('homeapp:home'))


def choose(request):

    return render(request, 'analysisapp/choose.html')
