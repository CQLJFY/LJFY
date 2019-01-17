from django.shortcuts import render
from django.views.generic.base import View

from .models import Surveyattribute,Surveyfile,CheckInformation

# Create your views here.

class pj_data(View):
    def get(self, request):
        search=request.GET.get("search","")
        if search:
            all_pj=Surveyattribute.objects.filter(pjid__icontains=search)
            title_pj = Surveyattribute.objects.filter(pjid__icontains=search)[:1]
        else:
            all_pj=None
            title_pj=None

        return render(request, 'data_search.html', {
            "all_pj":all_pj,
            "title_pj":title_pj,
        })

