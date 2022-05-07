from django.db import models
from django.db.models.fields import CharField, IntegerField, \
    TextField, DateField, DateTimeField, FloatField


# from review import analysisapp

label_name = 'homeapp'


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

    id = IntegerField(primary_key=True, auto_created=True)
    user_id = CharField(max_length=30)
    search_name = CharField(max_length=30)
    search_company = CharField(max_length=30)
    search_date = DateTimeField(auto_now=True)

    class Meta:
        db_table = 'MemberLog'
        app_label = label_name
        managed = False


class ArticleCode(models.Model):

    article_id = IntegerField(primary_key=True, auto_created=True)
    search_company = CharField(max_length=30)
    search_name = CharField(max_length=30)

    class Meta:
        db_table = 'ArticleCode'
        app_label = label_name
        managed = False


class ArticleInfo(models.Model):

    id = IntegerField(primary_key=True, auto_created=True)
    article_id = IntegerField()
    article_review_cnt = IntegerField()
    advertise_percent = FloatField()
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


class BuyList(models.Model):

    id = IntegerField(primary_key=True, auto_created=True)
    article_id = IntegerField()
    url = TextField()
    title = TextField()
    price = IntegerField()
    mall_name = CharField(max_length=30)
    image_url = TextField()

    class Meta:
        db_table = 'BuyList'
        app_label = label_name
        managed = False


class ReviewData(models.Model):

    review_id = IntegerField(primary_key=True, auto_created=True)
    article_id = IntegerField()
    advertise = IntegerField()
    url = TextField()
    title = TextField()
    writer = CharField(max_length=50)
    content = TextField()
    description = TextField()
    first_img_url = TextField()
    last_img = TextField()
    content_date = DateField()

    class Meta:
        db_table = 'ReviewData'
        app_label = label_name
        managed = False


class ReviewAnalysis(models.Model):

    id = IntegerField(primary_key=True, auto_created=True)
    article_id = IntegerField()
    summary = TextField()
    associate_url1 = TextField()
    associate_url2 = TextField()
    associate_url3 = TextField()

    class Meta:
        db_table = 'ReviewAnalysis'
        app_label = label_name
        managed = False
