from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField, IntegerField, TextField

CHOICE_CLASS = (('subscribed', 'subscribed'), ('unsubscribed', 'unsubscribed'))

# class Member(AbstractUser):
#     nickname = models.CharField(max_length=100)
#     userclass = models.CharField(
#         max_length=50,
#         choices=CHOICE_CLASS, 
#         default='unsubscribed',
#     )

label_name = 'accountapp'

class Member(models.Model):
    user_id = CharField(max_length = 30, primary_key=True)
    user_pw = CharField(max_length = 30)
    user_email = CharField(max_length = 30)
    user_nickname = CharField(max_length = 30)
    user_class = IntegerField()

    class Meta:
        db_table = 'User'
        app_label = label_name
        managed = False
