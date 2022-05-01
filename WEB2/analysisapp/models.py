from typing import Text
from django.db import models
from django.db.models.fields import CharField, IntegerField, TextField, DateField, DateTimeField


# from review import analysisapp

label_name = 'analysisapp'


class Member(models.Model):
    user_id = CharField(max_length=30, primary_key=True)
    user_pw = CharField(max_length=30)
    user_email = CharField(max_length=30)
    user_nickname = CharField(max_length=30)
    user_class = IntegerField()
    user_status = IntegerField()
    create_time = DateField(auto_now_add=True)
    update_time = DateField(auto_now=True)
    user_sex = IntegerField()
    user_birth = DateField()

    class Meta:
        db_table = 'Member'
        app_label = label_name
        managed = False


class MemberLog(models.Model):
    # primary key
    id = IntegerField(primary_key=True, auto_created=True)
    # 유저 아이디
    user_id = CharField(max_length=30)

    # 검색된 게시물 이름
    search_name = CharField(max_length=30)

    # 검색된 회사 이름
    search_company = CharField(max_length=30)

    # 검색된 날짜
    search_date = DateTimeField(auto_now=True)

    class Meta:
        db_table = 'MemberLog'
        app_label = label_name
        managed = False


# 검색 물품 기록


class ArticleCode(models.Model):
    # primary key
    article_id = IntegerField(primary_key=True, auto_created=True)
    # 회사 이름
    search_company = CharField(max_length=30)

    # 검색된 게시물 이름
    search_name = CharField(max_length=30)

    class Meta:
        db_table = 'ArticleCode'
        app_label = label_name
        managed = False


# 검색 물품 기록
class ArticleInfo(models.Model):
    # primary key
    id = IntegerField(primary_key=True, auto_created=True)
    # 검색된 게시물 이름
    article_id = IntegerField()
    # 리뷰 게시물 개수
    article_review_cnt = IntegerField()
    # 순수 리뷰 게시물 개수
    article_pure_review_cnt = IntegerField()
    # 검색 카운트
    search_cnt = IntegerField()

    img_url = TextField()

    twenty_male_cnt = IntegerField()
    twenty_female_cnt = IntegerField()

    fourty_male_cnt = IntegerField()
    fourty_female_cnt = IntegerField()

    class Meta:
        db_table = 'ArticleInfo'
        app_label = label_name
        managed = False


# 구매 데이터 크롤링
class BuyList(models.Model):
    # primary_key
    id = IntegerField(primary_key=True, auto_created=True)
    # 고유 코드
    article_id = IntegerField()
    # 구매링크
    url = TextField()
    # 구매 가격
    title = TextField()

    price = IntegerField()
    # 구매 장소
    mall_name = CharField(max_length=30)

    image_url = TextField()

    class Meta:
        db_table = 'BuyList'
        app_label = label_name
        managed = False

 # 리뷰 데이터 크롤링


class ReviewData(models.Model):

    review_id = IntegerField(primary_key=True, auto_created=True)
    # 검색물품의 코드
    article_id = IntegerField()
    # 글작성자
    writer = CharField(max_length=30)
    # 글내용
    content = TextField()
    # 글 쓴 날짜
    content_date = DateField()
    # 처음이미지
    first_img_url = TextField()
    # 마지막 이미지
    last_img_url = TextField()

    url = TextField()
    # 광고 분류
    advertise = IntegerField()

    description = TextField()
    title = TextField()

    class Meta:
        db_table = 'ReviewData'
        app_label = label_name
        managed = False

 # 리뷰 데이터 분석결과


class ReviewAnalysis(models.Model):
    # primary key
    id = IntegerField(primary_key=True, auto_created=True)
    # 블로그 게시글 고유 코드
    article_id = IntegerField()
    # 글요약
    summary = TextField()
    # 감정어 url
    emotion_url = TextField()
    # URL 주소
    associate_url = TextField()

    class Meta:
        db_table = 'ReviewAnalysis'
        app_label = label_name
        managed = False
