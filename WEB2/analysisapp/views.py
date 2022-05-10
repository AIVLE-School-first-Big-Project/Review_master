import secret_key as sk
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from analysisapp.models import ArticleCode, ArticleInfo,\
    BuyList, ReviewData, ReviewAnalysis, MemberLog,\
    Member, ReviewSentiment, ReviewSentimentDetail
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .crawling import crawling_function
from django.urls import reverse
import requests
import os
import sys
import zipfile
from datetime import date
from io import BytesIO
from pathlib import Path
import random

from dateutil.relativedelta import relativedelta
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

BASE_DIR1 = Path(__file__).resolve().parent.parent.parent

con = sk.config()
Backend_filtering = "http://" + \
    con.get_secret("HOST") + ":" + con.get_secret("API_PORT") + "/filtering/"
Backend_summary = "http://" + \
    con.get_secret("HOST") + ":" + con.get_secret("API_PORT") + "/summary/"
Backend_association = "http://" + \
    con.get_secret("HOST") + ":" + con.get_secret("API_PORT") + "/association/"
Backend_sentiment = "http://" + \
    con.get_secret("HOST") + ":" + con.get_secret("API_PORT") + "/sentiment/"

Backend_explainImage = "http://" + \
    con.get_secret("HOST") + ":" + con.get_secret("API_PORT") + "/explain/"


def age_group_check(birth_date):

    age = relativedelta(
        date.today(), datetime.strptime(str(birth_date), "%Y-%m-%d"))

    if age.years < 40:
        return 0
    else:
        return 1


def rm_emoji1(Data):
    return Data.encode('euc-kr', 'ignore').decode('euc-kr')


@csrf_exempt
def result(request):
    if request.method == "GET":
        crawling_check = False
        login_id = request.session.get('user_id', "nonuser")

        print(f"현재 로그인한 사람 {login_id}")

        # 사용자가 검색한 경우
        search_company = request.GET.get("company", 0)
        search_name = request.GET.get("article_name", 0)

        # 검색 결과 로그 출력
        # print(search_company)
        # print(search_name)

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
                m_article_info = ArticleCode.objects.filter(
                    Q(search_company=search_company)
                    & Q(search_name=search_name))

            article_id = m_article_info[0].article_id

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
                crawling_check = True
                df = crawling_function.service_start(
                    search_company, search_name)

                try:
                    df["내돈내산 키워드"]
                except Exception:
                    m_article_info = ArticleInfo.objects.get(
                        article_id=article_id)
                    m_article_info.delete()

                    m_article_code = ArticleCode.objects.get(
                        article_id=article_id)
                    m_article_code.delete()

                    return HttpResponseRedirect(reverse('homeapp:home'))

                url, title, post_date, description, writer, content, \
                    first_img_url, last_img_url \
                    = df["url"], df["title"], df["post_date"],\
                    df["description"], df["writer"], df["content"], \
                    df["first_img"], df["last_img"]

                content_cnt, content_line, quote_cnt, img_cnt,\
                    coupang, ndns, dj, sj, bg, dot, b, z, zz, zzzz\
                    = df["content_cnt"], df["content_line"],\
                    df["quote_cnt"], df["img_cnt"],\
                    df["coupa.ng 키워드"], df["내돈내산 키워드"], df["단점 빈도 수"],\
                    df["솔직 빈도 수"],  df["비교 빈도 수"], df["... 빈도 수"], \
                    df["ㅠ 빈도 수"], df["ㅋ 빈도 수"], \
                    df["ㅋㅋ 빈도 수"], df["ㅋㅋㅋㅋ 빈도 수"]
                # blog_cnt = len(df)
                review_cnt = df.shape[0]

                # print(review_cnt)

                # 리뷰 데이터가 얼마나 있는지 확인하고 저장
                m_article_info = ArticleInfo.objects.get(article_id=article_id)
                m_article_info.article_review_cnt = review_cnt
                m_article_info.save()
                for idx, i in enumerate(range(len(df))):
                    cot = rm_emoji1(content[i])
                    tit = rm_emoji1(title[i])
                    dsec = rm_emoji1(description[i])
                    m_review_data = ReviewData()
                    m_review_data.article_id = article_id
                    m_review_data.writer = writer[i]
                    m_review_data.content = cot
                    m_review_data.content_date = post_date[i]
                    m_review_data.first_img_url = first_img_url[i]
                    m_review_data.last_img = last_img_url[i]
                    m_review_data.title = tit
                    m_review_data.url = url[i]
                    m_review_data.description = dsec

                    # 광고 필터링 API 보내기.
                    """"
                        1. 글 데이터 특징 추출
                        2. 이미지 데이터 특징 추출
                    """
                    # 보낼 데이터 양식
                    # 51 -> pro
                    # 1 -> pred

                    print(f"{idx} / {len(df)} 필터링 시작합니다.")
                    m_review_data.save()

                    m_review_data = ReviewData.objects.get(
                        article_id=article_id, writer=writer[i],
                        url=url[i], content_date=post_date[i])
                    data = {
                        "review_id": [str(m_review_data.review_id)],
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
                        "ㅠ 빈도 수": [int(b[i])],
                        "ㅋㅋ 빈도 수": [int(zz[i])]
                        # "ㅠㅠ 빈도 수": [int(bb[i])],
                        # "ㅋㅋㅋ 빈도 수": [int(zzz[i])]
                    }
                    response = requests.post(Backend_filtering, json=data)
                    if response.status_code == 200:
                        filter_data = response.json()["pred"]
                        filter_percent = response.json()["pro"]

                    m_review_data.advertise = int(filter_data)
                    m_review_data.advertise_percent = float(
                        filter_percent)  # 확률 처리
                    m_review_data.save()

                    if int(filter_data) == 0:  # 순수다
                        m_article_info = ReviewData.objects.get(
                            article_id=article_id,
                            writer=writer[i], first_img_url=first_img_url[i])
                        review_id = m_article_info.review_id

                        m_review_sentiment = ReviewSentiment()
                        m_review_sentiment.review_id = review_id
                        m_review_sentiment.article_id = article_id

                        # print(review_id)
                        # print(article_id)

                        data = {
                            "artice_code": int(article_id),
                            "review_id": int(review_id)
                        }
                        response = requests.post(Backend_sentiment,
                                                 params=data,
                                                 headers={
                                                     'accept':
                                                     'application/json'
                                                     })
                        negative = response.json()["negative"]
                        positive = response.json()["positive"]

                        result = response.json()["blog_result"]

                        m_review_sentiment.positive = positive
                        m_review_sentiment.negative = negative

                        m_review_sentiment.save()

                        m_reivew_sentiment = ReviewSentiment.objects.filter(
                            review_id=review_id, article_id=article_id,
                            positive=positive, negative=negative)
                        try:
                            sentiment_id = m_reivew_sentiment[0].sentiment_id
                        except Exception:
                            pass
                        positive_len = 0
                        negative_len = 0
                        for i in range(len(result)):
                            m_review_sentiment_detail = \
                                ReviewSentimentDetail()
                            m_review_sentiment_detail.sentiment_id = \
                                sentiment_id
                            m_review_sentiment_detail.content = str(
                                result[i][0])
                            m_review_sentiment_detail.sentiment = result[i][1]

                            if result[i][1] == 1:
                                if positive_len > 10:
                                    continue
                                positive_len += 1
                            else:
                                if negative_len > 10:
                                    continue
                                negative_len += 1

                            m_review_sentiment_detail.save()

            # buylist 추가하기
            m_buy_list = BuyList.objects.filter(article_id=article_id)

            if len(m_buy_list) == 0:  # 아무것도 없는 경우
                title, url, image_url, price, mall_name = \
                    crawling_function.service_buy(search_company, search_name)

                # 만약 가격차이가 너무 나는 경우는 원하는 값이 아닐수도 있다.

                average_price = (sum(price) + 1) / (len(price) + 1)

                for i in range(len(title)):

                    if average_price * 0.5 <= price[i] <= average_price * 1.5:
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
                    'artice_code': article_id,
                }
                response = requests.post(Backend_summary, params=item2)
                if response.status_code == 200:
                    print("요약 결과")
                    summary_data = response.json()["Decs"]
                    # print(summary_data)

                response = requests.post(Backend_association, params=item2)
                print("경로 : ", BASE_DIR1)
                association_paths = ""
                if response.status_code == 200:
                    print("연관어 결과")
                    suvey_zip = zipfile.ZipFile(BytesIO(response.content))
                    suvey_zip.extractall(os.path.join(BASE_DIR1, "WEB2/media"))
                    association_paths = [
                        "/media/"+suvey_zip.filelist[i].
                        filename for i in range(len(suvey_zip.filelist))]
                m_review_analysis = ReviewAnalysis()
                m_review_analysis.article_id = article_id
                m_review_analysis.summary = summary_data
                if association_paths == "" or len(association_paths) == 0:
                    m_review_analysis.associate_url1 = ""
                    m_review_analysis.associate_url2 = ""
                    m_review_analysis.associate_url3 = ""
                elif len(association_paths) == 3:
                    m_review_analysis.associate_url1 = association_paths[0]
                    m_review_analysis.associate_url2 = association_paths[1]
                    m_review_analysis.associate_url3 = association_paths[2]
                elif len(association_paths) == 2:
                    m_review_analysis.associate_url1 = association_paths[0]
                    m_review_analysis.associate_url2 = association_paths[1]
                    m_review_analysis.associate_url3 = ""
                elif len(association_paths) == 1:
                    m_review_analysis.associate_url1 = association_paths[0]
                    m_review_analysis.associate_url2 = ""
                    m_review_analysis.associate_url3 = ""

                m_review_analysis.save()

            m_article_info = ArticleInfo.objects.get(article_id=article_id)

            data_info = {}
            data_info["company"] = search_company
            data_info["name"] = search_name
            data_info["review_cnt"] = m_article_info.article_review_cnt

            try:
                requests.get(m_article_info.img_url)
                data_info["img_url"] = m_article_info.img_url
            except Exception:
                data_info["img_url"] = ""

            review_list = []
            m_review_data = ReviewData.objects.filter(
                article_id=article_id).order_by("advertise_percent")

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
                    "advertise_percent": [],
                    "positive": [],
                    "negative": [],
                    "sentiment_id": []
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
                try:
                    advertise_percent = int(review.advertise_percent) * 100
                except Exception:
                    advertise_percent = 100
                review_dict["advertise_percent"] = advertise_percent
                # 현재 이 값은 광고일 확률을 알려준다.
                try:
                    if int(review.advertise) != 0:
                        review_cnt -= 1
                        continue
                except Exception:
                    review_cnt -= 1
                    continue

                if len(review_list) == 10:
                    continue
                try:
                    m_review_sentiment = ReviewSentiment.objects.get(
                        review_id=review.review_id,
                        article_id=review.article_id)
                    pos = m_review_sentiment.positive
                    neg = m_review_sentiment.negative
                    if pos == 0 and neg == 0:
                        pos_per = 0
                        neg_per = 0
                    elif pos == 0 and neg != 0:
                        pos_per = 0
                        neg_per = 100
                    elif pos != 0 and neg == 0:
                        pos_per = 100
                        neg_per = 0
                    else:
                        pos_per = int((pos / (neg+pos)) * 100)
                        neg_per = 100 - pos_per
                    review_dict["positive"] = pos_per
                    review_dict["negative"] = neg_per
                    review_dict["sentiment_id"] = \
                        m_review_sentiment.sentiment_id
                except ReviewSentiment.DoesNotExist:
                    pass

                review_list.append(review_dict)

            data_info["pure_cnt"] = review_cnt

            analysis_list = {}
            m_review_analysis = ReviewAnalysis.objects.get(
                article_id=article_id)

            analysis_list["summary"] = m_review_analysis.summary
            analysis_list["associate_url1"] = m_review_analysis.associate_url1
            analysis_list["associate_url2"] = m_review_analysis.associate_url2
            analysis_list["associate_url3"] = m_review_analysis.associate_url3

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


def detail(request, sentiment_id):
    m_review_sentiment = ReviewSentimentDetail.objects.filter(
        sentiment_id=sentiment_id)

    m_review = ReviewSentiment.objects.get(
        sentiment_id=m_review_sentiment[0].sentiment_id)

    positive_list = []
    negative_list = []
    positive_list = []
    negative_list = []
    positive_lists = []
    negative_lists = []
    for i in m_review_sentiment:
        if i.sentiment == 0:
            negative_lists.append(i.content)
        else:
            positive_lists.append(i.content)
    if len(negative_lists) > 5:
        negative_num = random.sample(
            [i for i in range(len(negative_lists))], 5)
    else:
        negative_num = random.sample(
            [i for i in range(len(negative_lists))], len(negative_lists))

    if len(positive_lists) > 5:
        positive_num = random.sample(
            [i for i in range(len(positive_lists))], 5)
    else:
        positive_num = random.sample(
            [i for i in range(len(positive_lists))], len(positive_lists))

    for idx, i in enumerate(negative_num):
        negative_list.append({
            "idx": idx+1,
            "content": negative_lists[i]
        })
    for idx, i in enumerate(positive_num):
        positive_list.append({
            "idx": idx+1,
            "content": positive_lists[i]
        })
    m_review_data = ReviewData.objects.get(review_id=m_review.review_id)
    m_article_code = ArticleCode.objects.get(
        article_id=m_review_data.article_id)
    review_list = {
        "url": m_review_data.url,
        "title": m_review_data.title,
        "description": m_review_data.description,
        "first_img_url": m_review_data.first_img_url,
        "company": m_article_code.search_company,
        "article_name": m_article_code.search_name

    }

    return render(request, 'analysisapp/detail.html', {
        "review_id": m_review.review_id,
        "positive_list": positive_list,
        "negative_list": negative_list,
        "review_list": review_list
    })
