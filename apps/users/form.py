__author__ = 'zhu'
__date__ = '2019/1/17 10:09'

from django import forms

class LoginForm(forms.Form):
    username=forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)