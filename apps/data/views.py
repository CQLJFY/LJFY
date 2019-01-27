import json
import zipfile
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
                dic = {'idsurveyattribute':i.said.idsurveyattribute,'pjid':i.said.pjid,'pjname':i.said.pjname,
                       'filepath': i.filepath, 'surveyperson': i.said.surveyperson, 'filetype': i.said.filetype,
                       'isanalysed': i.said.isanalysed, 'all_check': all_check,'flag':flag}
                list.append(dic)

            # 取出所有的测量员
            all_person = [person.surveyperson for person in Surveyattribute.objects.all()]
            # 去重
            all_person = set(all_person)

        else:
            title_pj=None
            list=[]
            all_person=None

        return render(request, 'test2.html', {
            "title_pj":title_pj,
            "list":list,
            "all_person":all_person,
        })


def files_download(request,idsurveyattribute,type):
    '''判断type，把对应的数据写成文件并下载，1是分析报告，2是点位数据，3是外业文件'''
    def zip_ya(startdir,file_news):
        '''文件压缩'''
        z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
        for dirpath, dirnames, filenames in os.walk(startdir):
            fpath = dirpath.replace(startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
        z.close()
    new_file_path = '' #每个文件最终的绝对路径
    file_name=''
    file_path=''# 工程文件夹的绝对路径
    obj = Surveyfile.objects.filter(Q(said__idsurveyattribute=idsurveyattribute),
                                    Q(filepath__contains='.cpf') |
                                    Q(filepath__contains='.svy') |
                                    Q(filepath__contains='.dc'))
    for i in obj:
        file_path = "F:\\LJFY\\files_download\\" + i.said.pjid + '\\' + i.said.surveyperson + '\\' \
                        + i.said.filetype + '\\'
        if not os.path.exists(file_path):  # 判断文件夹是否存在
            os.makedirs(file_path)  # 创建文件
    if type=='1':
        # 取出工程文件
        for i in obj:
            # 将文件路径简化
            i.filepath = i.filepath.split('\\')[7:]
            str = ' / '
            i.filepath = str.join(i.filepath)
            # 完成状态映射
            if i.said.isanalysed == 1:
                i.said.isanalysed = '已分析'
            elif i.said.isanalysed == 0:
                i.said.isanalysed = '未分析'
            else:
                i.said.isanalysed = '文件不全'
            # 将检查数据写成文件
            all_check = CheckInformation.objects.filter(source__idsurveyattribute=idsurveyattribute). \
                order_by("-log_level")
            with open(file_path + '分析报告.txt', 'w') as f:
                for j in all_check:
                    f.write(j.source.pjid + ' ' + j.source.pjname + '  数据类型：' + j.source.filetype + '  状态：'+ i.said.isanalysed+ '\n')
                    f.write(i.filepath + '\n')
                    for x in all_check:
                        f.write(x.log_level + ' : ' + x.check_category  + '   ' + x.information+ '   ' + x.detail + '   ' + '\n')
                    break
        file_name = "分析报告.txt"  # 文件名
        new_file_path = os.path.join(file_path,file_name)  # 下载文件的绝对路径
    elif type=='2':
        # 取出点位数据
        file_points = Points2018.objects.filter(source__idsurveyattribute=idsurveyattribute)
        with open(file_path + '点位数据.txt', 'w') as f:
            for i in file_points:
                f.write(i.wkbgeometry + ',' + i.source.pjid)
                f.write('\n')
        file_name = "点位数据.txt"  # 文件名
        new_file_path = os.path.join(file_path, file_name)  # 下载文件的绝对路径
    else:
        # 取出外业文件
        all_files = Surveyfile.objects.filter(said__idsurveyattribute=idsurveyattribute)
        # 将外业文件写出来
        for i in all_files:
            path = os.path.split(i.filepath)
            file_name =path[1]  # 文件名
            new_file_path = os.path.join(file_path, '外业文件\\')  # 下载文件的绝对路径
            if not os.path.exists(new_file_path):  # 判断文件夹是否存在
                os.makedirs(new_file_path)
            with open(new_file_path+file_name, 'wb') as f:
                f.write(bytes(i.content))
        name=os.path.join(file_path, '外业原始文件.zip')
        zip_ya(new_file_path,name)
        file_name='外业原始文件.zip'
        new_file_path = os.path.join(file_path, '外业原始文件.zip')  # 下载文件的绝对路径

    if not os.path.isfile(new_file_path):  # 判断下载文件是否存在
        return HttpResponse("Sorry but Not Found the File")

    def file_iterator(file_path, chunk_size=512):
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    try:
        # 设置响应头
        # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
        response = StreamingHttpResponse(file_iterator(new_file_path))
        # 以流的形式下载文件,这样可以实现任意格式的文件下载
        response['Content-Type'] = 'application/octet-stream'
        # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)
    except:
        return HttpResponse("Sorry but Not Found the File")
    return response
