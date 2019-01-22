from django.shortcuts import render, HttpResponse,render_to_response
from django.http import StreamingHttpResponse
from django.db.models import Q
from django.views.generic.base import View

from .models import Surveyattribute,Surveyfile,CheckInformation

# Create your views here.

class pj_data(View):
    def get(self, request):
        search=request.GET.get("search","")
        if search:
            # 取出搜索工程的所有文件
            all_pj=Surveyfile.objects.filter(Q(said__pjid__icontains=search),
                                             Q(filepath__contains='.cpf')|
                                             Q(filepath__contains='.svy')|
                                             Q(filepath__contains='.dc'))
            # 截取文件名并对状态进行映射
            for i in all_pj:
                i.filepath=i.filepath.split('\\')[-1]
                if i.said.isanalysed==1:
                    i.said.isanalysed ='已分析'
                elif i.said.isanalysed==0:
                    i.said.isanalysed ='未分析'
                else:
                    i.said.isanalysed='文件不全'

            # 取出工程编号和工程名称
            title_pj = Surveyattribute.objects.filter(pjid__icontains=search)[:1]
            # 取出搜索工程的检查信息
            # all_check = CheckInformation.objects.filter(said__pjid__icontains=search)
        else:
            all_pj=None
            title_pj=None
            all_check=None

        return render(request, 'data_search.html', {
            "all_pj":all_pj,
            "title_pj":title_pj,
            # "all_check":all_check,
        })


class file_down(View):
    '''
    文件下载功能
    '''
    def get(self,request):
        pass
        return render_to_response()
