from django.db import models
from django.db.models.fields import CharField, IntegerField, TextField, DateTimeField
from accountapp.models import Member
from datetime import datetime

# Create your models here.
label_name = 'board'


class QABoard(models.Model):
    id = IntegerField(primary_key=True, auto_created=True)
    user_id = CharField(max_length=150)
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
