from django.db import models
from django.db.models.fields import CharField, IntegerField, TextField, DateTimeField

label_name = 'homeapp'

class Member(models.Model):
    user_id = CharField(max_length = 30, primary_key=True)
    user_pw = CharField(max_length = 30)
    user_email = CharField(max_length = 30)
    user_nickname = CharField(max_length = 30)
    user_class = IntegerField()
    user_status = IntegerField()
    create_time = DateTimeField(auto_now_add=True)
    update_time = DateTimeField(auto_now=True)
    user_sex = IntegerField()
    user_birth = DateTimeField()

    class Meta:
        db_table = 'Member'
        app_label = label_name
        managed = False

class QABoard(models.Model):
    id = IntegerField(primary_key=True)
    user = models.ForeignKey('Member', on_delete=models.CASCADE)
    # answer_user = models.ForeignKey('Member', on_delete=models.CASCADE)
    title = TextField()
    content = TextField()
    answer_title = TextField()
    answer_content = TextField()
    create_time = DateTimeField(auto_now_add=True)
    update_time = DateTimeField(auto_now=True)
    # answer_time = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'QABoard'
        app_label = label_name
        managed = False