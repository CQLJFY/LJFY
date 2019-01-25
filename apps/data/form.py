__author__ = 'zhu'
__date__ = '2019/1/25 11:03'

from django import forms

from .models import Surveyattribute


class SurveypersonForm(forms.ModelForm):
    class Meta:
        model = Surveyattribute
        fields = ['surveyperson']