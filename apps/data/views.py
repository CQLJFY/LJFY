from django.shortcuts import render
from django.views.generic.base import View

from .models import Surveyattribute,Surveyfile,CheckInformation

# Create your views here.

class pj_data(View):
    def get(self, request):
        pass

        return render(request, 'data_search.html', {

        })

