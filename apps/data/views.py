from django.shortcuts import render,render_to_response
from django.db.models import Q
from django.views.generic.base import View
from itertools import chain

from .models import Surveyattribute,Surveyfile,CheckInformation

# Create your views here.

class pj_data(View):
    # 数据查询
    def get(self, request):
        search=request.GET.get("search","")
        test=None
        if search:
            # 取出搜索工程的所有文件
            all_pj=Surveyfile.objects.filter(Q(said__pjid__icontains=search),
                                             Q(filepath__contains='.cpf')|
                                             Q(filepath__contains='.svy')|
                                             Q(filepath__contains='.dc')).order_by("idsurveyfile")
            # 截取文件名并对状态进行映射
            for i in all_pj:
                i.filepath=i.filepath.split('\\')[7:]
                str=' / '
                i.filepath=str.join(i.filepath)
                if i.said.isanalysed==1:
                    i.said.isanalysed ='已分析'
                elif i.said.isanalysed==0:
                    i.said.isanalysed ='未分析'
                else:
                    i.said.isanalysed='文件不全'
            #     取出检查信息并合并
            #     all_check = CheckInformation.objects.filter(source__idsurveyattribute=i.said.idsurveyattribute).order_by("-log_level")
            #     all_pj=chain(i,all_check)
            # 取出工程编号和工程名称
            title_pj = Surveyattribute.objects.filter(pjid__icontains=search)[:1]
            # 取出搜索工程的检查信息
            all_check = CheckInformation.objects.filter(source__pjid__icontains=search).order_by("-log_level")

        else:
            all_pj=None
            title_pj=None
            all_check=None

        return render(request, 'test2.html', {
            "all_pj":all_pj,
            "title_pj":title_pj,
            "all_check":all_check,
        })


class file_down(View):
    '''
    文件下载功能
    '''
    def get(self,request):
        pass
        return render_to_response()
