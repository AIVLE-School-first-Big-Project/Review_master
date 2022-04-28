from django import forms
from .models import Member

class searchForm(forms.Form):
    search_item = forms.CharField(max_length=150)