import json
from django.shortcuts import render,render_to_response
from django.db.models import Q
import os
from django.views.generic.base import View
from django.http import StreamingHttpResponse,HttpResponse

from .models import Surveyattribute,Surveyfile,CheckInformation,Points2018
from users.models import UserProfile
from .form import SurveypersonForm

# Create your views here.

class pj_data(View):
    # 数据查询
    def get(self, request):
        search=request.GET.get("search","")
        test=None
        if search:
            # 取出搜索工程的所有文件
            #  对权限进行判断
            if UserProfile.objects.filter(username=request.user)[0].user_type == "小组长":
                all_pj = Surveyfile.objects.filter(Q(said__pjid__icontains=search),
                                                   Q(said__surveyperson=request.user),
                                                   Q(filepath__contains='.cpf') |
                                                   Q(filepath__contains='.svy') |
                                                   Q(filepath__contains='.dc')).order_by("idsurveyfile")
                # 取出工程编号和工程名称
                title_pj = Surveyattribute.objects.filter(Q(pjid__icontains=search),
                                                          Q(surveyperson=request.user))[:1]
            else:
                all_pj = Surveyfile.objects.filter(Q(said__pjid__icontains=search),
                                                   Q(filepath__contains='.cpf') |
                                                   Q(filepath__contains='.svy') |
                                                   Q(filepath__contains='.dc')).order_by("idsurveyfile")
                # 取出工程编号和工程名称
                title_pj = Surveyattribute.objects.filter(pjid__icontains=search)[:1]
            # 截取文件名并对状态进行映射
            list=[]
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
                all_check = CheckInformation.objects.filter(source__idsurveyattribute=i.said.idsurveyattribute).\
                    order_by("-log_level")
                level_list=[check.log_level for check in all_check]
                if 'warn' in level_list:
                    flag=1
                else:
                    flag=None
                dic = {'pjid':i.said.pjid,'pjname':i.said.pjname,'filepath': i.filepath, 'surveyperson': i.said.surveyperson, 'filetype': i.said.filetype,
                       'isanalysed': i.said.isanalysed, 'all_check': all_check,'flag':flag}
                list.append(dic)

            # 取出所有的测量员
            all_person = [person.surveyperson for person in Surveyattribute.objects.all()]
            # 去重
            all_person = set(all_person)

            # 将所有需要下载的资料分别写出文件
            # 创建目录
            new_file_path=''
            for i in title_pj:
                new_file_path = 'F:\\文件下载\\' + i.pjid + '\\' + i.surveyperson + '\\' \
                                + i.filetype + '\\'
                if os.path.exists(new_file_path):  #判断文件是否存在
                    break
                else:
                    os.makedirs(new_file_path)  #创建文件
            # 取出外业文件
            if UserProfile.objects.filter(username=request.user)[0].user_type == "小组长":
                all_files = Surveyfile.objects.filter(Q(said__pjid__icontains=search),Q(said__surveyperson=request.user))
            else:
                all_files = Surveyfile.objects.filter(said__pjid__icontains=search)
            # 将外业文件写出来
            for i in all_files:
                file_path = os.path.split(i.filepath)
                with open(new_file_path + file_path[1],'wb') as f:
                    f.write(bytes(i.content))

            # 取出点位数据
            file_points=Points2018.objects.filter(source__pjid__icontains=search)
            with open(new_file_path + '点位数据.txt','w') as f:
                for i in file_points:
                    f.write(i.wkbgeometry+','+i.source.pjid)
                    f.write('\n')
            # 取出分析结果
            with open(new_file_path + '分析报告.txt','w') as f:
                for i in list:
                    f.write(i['pjid']+' '+i['pjname']+' 数据类型：'+i['filetype']+' 状态：'+i['isanalysed']+'\n')
                    f.write(i['filepath']+'\n')
                    for j in i['all_check']:
                        f.write(j.log_level+' : '+j.check_category+'  '+j.detail+'  '+ '\n')
                    f.write('\n')




        else:
            title_pj=None
            list=[]
            all_person=None

        return render(request, 'test2.html', {
            "title_pj":title_pj,
            "list":list,
            "all_person":all_person,
        })