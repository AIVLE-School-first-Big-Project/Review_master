from django import forms


class searchForm(forms.Form):
    search_item = forms.CharField(max_length=150)
