from django.db import models
from django.db.models.fields import CharField, IntegerField, TextField,DateTimeField

label_name = 'accountapp'

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
