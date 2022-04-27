from django.db import models
from django.db.models.fields import CharField, IntegerField

# from review import analysisapp

label_name='analysisapp'

# 검색 물품 기록
class ArticleInfo(models.Model):
    # primary key
    article_code= models.IntegerField(primary_key=True)
    #검색된 게시물 이름
    search_name=models.CharField(max_length=30)
    # 리뷰 게시물 개수
    article_review_cnt= models.IntegerField()
    #순수 리뷰 게시물 개수
    article_pure_review_cnt= models.IntegerField()
    #검색 카운트
    search_cnt= models.IntegerField()
    class Meta:
        db_table = 'ArticleInfo'
        app_label = label_name
        managed = False



 # 리뷰 데이터 크롤링
class ReviewData(models.Model):
     # 블로그 게시글 고유코드 primary_key
    blog_code = models.IntegerField(primary_key=True)
    # 검색물품의 코드
    article_code=models.ForeignKey(ArticleInfo,on_delete=models.CASCADE,db_column='article_code')
    # 글작성자
    writer = models.CharField(max_length=30)
     # 글내용
    content = models.TextField()
    # 글 쓴 날짜
    content_date = models.DateField()
    # 처음이미지
    first_img_url = models.CharField(max_length=255)
     # 마지막 이미지
    last_img_url = models.CharField(max_length=255)
    class Meta:
        db_table = 'ReviewData'
        app_label = label_name
        managed = False


 # 리뷰 데이터 분석결과
class ReviewAnalysis(models.Model):
     # primary key
    id = models.IntegerField(primary_key=True)
     # 블로그 게시글 고유 코드
    blog_code=models.ForeignKey("ReviewData",on_delete=models.CASCADE,db_column='blog_code')
     #광고 분류
    advertise=models.IntegerField()
    #글요약
    summary=models.TextField()
    #긍정적인글
    positive=models.TextField()
     #부정적인글
    negative=models.TextField()
    # URL 주소
    associate_url=models.TextField()

    class Meta:
        db_table = 'ReviewAnalysis'
        app_label = label_name
        managed = False

        
# 구매 데이터 크롤링
class BuyList(models.Model):
    # primary_key
    id = models.IntegerField(primary_key=True)
    # 블로그 게시글 고유 코드
    article_code=models.ForeignKey("ArticleInfo",on_delete=models.CASCADE,db_column='article_code')
    # 구매링크
    url = models.TextField()
    # 구매 가격
    price = models.IntegerField()
    # 구매 장소
    market_name=models.CharField(max_length=30)
    # 크롤링한 시간
    create_time=models.DateField()
    class Meta:
        db_table = 'BuyList'
        app_label = label_name
        managed = False
