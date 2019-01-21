from django.shortcuts import render, HttpResponse,render_to_response
from django.http import StreamingHttpResponse

from django.views.generic.base import View

from .models import Surveyattribute,Surveyfile,CheckInformation

# Create your views here.

class pj_data(View):
    def get(self, request):
        search=request.GET.get("search","")
        if search:
            # 取出搜索的所有工程
            all_pj=Surveyattribute.objects.filter(pjid__icontains=search)
            # 取出搜索工程的id
            said_ids=[pj.idsurveyattribute for pj in all_pj]
            # 取出搜索工程的所有文件
            all_file=Surveyfile.objects.filter(said__pjid__icontains=search)

            title_pj = Surveyattribute.objects.filter(pjid__icontains=search)[:1]
        else:
            all_pj=None
            title_pj=None
            all_file=None


        return render(request, 'data_search.html', {
            "all_pj":all_pj,
            "title_pj":title_pj,
            "all_file":all_file
        })


class file_down(View):
    '''
    文件下载功能
    '''
    def get(self,request):
        pass
        return render_to_response()
