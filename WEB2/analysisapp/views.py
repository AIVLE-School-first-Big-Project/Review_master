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
import requests, os,sys,json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import secret_key as sk



con = sk.config()
Backend_filtering = "http://"+con.get_secret("HOST") +":"+ con.get_secret("API_PORT") +"/filtering/"
Backend_summary = "http://"+con.get_secret("HOST") +":"+ con.get_secret("API_PORT") +"/summary/"

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

            # 검색 기록 남기기
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
            if crawling_check:
                print("해당 코드가 아직 저장이 안되어있음")
                m_article_info = ArticleInfo()
                m_article_info.article_id = article_id
                m_article_info.search_cnt = 1
                m_article_info.img_url = crawling_function.service_img(
                    search_company, search_name)
                m_article_info.save()

            else:
                ## 상품 등록을 시켜주는 역할.
                m_article_info = ArticleInfo.objects.get(article_id=article_id)
                m_article_info.search_cnt += 1
                m_article_info.save()

            # 크롤링 진행 혹은 리뷰 데이터 가져오기
            review = ReviewData.objects.filter(article_id=article_id)   # 리뷰 테이블에서 데이터 가져오기.

            # 데이터가 하나도 없는 경우 이거나 위에서 크롤링해야한다고 한 경우 크롤링을 진행한다.
            if len(review) == 0 or crawling_check:
                df = crawling_function.service_start(
                    search_company, search_name)

                # Review Data에 데이터를 추가시켜주자. writer, content, description, content_date, first_img_url, last_img_url, url을 넣어준다.
                url, title, post_date, description, writer, content, first_img_url, last_img_url = df["url"], df[
                    "title"], df["post_date"], df["description"], df["writer"], df["content"], df["first_img"], df["last_img"]
                # blog_cnt = len(df)
                blog_cnt = df.shape[0]

                # 리뷰 데이터가 얼마나 있는지 확인하고 저장
                m_article_info = ArticleInfo.objects.get(article_id=article_id)
                m_article_info.article_review_cnt = blog_cnt
                m_article_info.save()
                print("데이터 저장")
                for i in range(len(df)):
                    m_review_data = ReviewData()
                    m_review_data.article_id = article_id
                    m_review_data.writer = writer[i]
                    m_review_data.content = content[i]
                    m_review_data.content_date = post_date[i]
                    m_review_data.first_img_url = first_img_url[i]
                    m_review_data.last_img_url = last_img_url[i]
                    m_review_data.url = url[i]
                    m_review_data.description = description[i]
                    m_review_data.advertise = 0
                    m_review_data.save()


            # 광고 필터링 API 보내기.
            """"
                1. 글 데이터 특징 추출
                2. 이미지 데이터 특징 추출
            """
            # 보낼 데이터 양식
            item1 = [1,2,3,4,5]
            response = requests.post(Backend_filtering, data =json.dumps(item1))
            print(Backend_filtering)
            print(response.status_code)
            if response.status_code == 200:
                print("필터링 결과")
                filter_data = response.json()["pred"]
                print(filter_data)

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
                response = requests.post(Backend_summary, params = item2)
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
            m_review_data = ReviewData.objects.filter(article_id=article_id)

            pure_cnt = int(data_info["review_cnt"])

            for review in m_review_data:
                review_dict = {
                    "writer": [],
                    "content": [],
                    "content_date": [],
                    "first_img_url": [],
                    "last_img_url": [],
                    "url": [],
                    "description": [],
                    "advertise": []
                }

                review_dict["writer"] = review.writer
                review_dict["content"] = review.content
                review_dict["content_date"] = review.content_date
                review_dict["first_img_url"] = review.first_img_url
                review_dict["last_img_url"] = review.last_img_url
                review_dict["url"] = review.url
                review_dict["description"] = review.description
                review_dict["advertise"] = review.advertise
                pure_cnt -= review.advertise
                review_list.append(review_dict)

            data_info["pure_cnt"] = pure_cnt

            analysis_list = {}
            m_review_analysis = ReviewAnalysis.objects.get(
                article_id=article_id)

            analysis_list["summary"] = m_review_analysis.summary
            analysis_list["emotion_url"] = m_review_analysis.emotion_url
            analysis_list["associate_url"] = m_review_analysis.associate_url

            return render(request, 'analysisapp/result.html', {
                "select_num": 1,
                "data_info": data_info,
                "review_list": review_list,
                "analysis_list": analysis_list
            })

    return HttpResponseRedirect(reverse('homeapp:home'))


def choose(request):
    return HttpResponseRedirect(reverse('homeapp:home'))
