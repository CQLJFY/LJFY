import json
import zipfile
from django.shortcuts import render,render_to_response
from django.db.models import Q
import os
from django.views.generic.base import View
from django.http import StreamingHttpResponse,HttpResponse
from django.utils.http import urlquote
from django.contrib.gis.geos import GEOSGeometry


from .models import Surveyattribute,Surveyfile,CheckInformation,Points2018
from users.models import UserProfile
from .form import SurveypersonForm

# Create your views here.

class pj_data(View):
    # print (os.path.abspath('.'))
    # 数据查询
    def get(self, request):
        search=request.GET.get("search","")
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
                # 对检查信息等级进行映射
                for j in all_check:
                    if j.log_level=='error':
                        j.log_level='错误'
                    elif j.log_level=='warn':
                        j.log_level='警告'
                    else:
                        j.log_level='信息'

                level_list=[check.log_level for check in all_check]
                if '错误' in level_list:
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

        return render(request, 'data_search.html', {
            "title_pj":title_pj,
            "list":list,
            "all_person":all_person,
        })


def files_download(request,idsurveyattribute,flag):
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

    zip_name=''
    file_path1=''# 外业文件夹的绝对路径
    file_path2 = ''#检查报告文件夹的绝对路径
    file_path3 = ''
    test=Surveyattribute.objects.filter(idsurveyattribute=idsurveyattribute)
    a=''
    for i in test:
        a=i.pjid
    obj=Surveyattribute.objects.filter(pjid=a)
    for i in obj:
        # 外业文件夹路径
        file_path1 = os.path.abspath('.')+"\\files_download\\" + i.pjid + '\\' + i.surveyperson + '\\' \
                    + i.filetype+ repr(i.idsurveyattribute) + '\\'+'外业文件'+'\\'
        # 检查报告文件夹路径
        file_path2=os.path.abspath('.')+"\\files_download\\" + i.pjid + '\\' + i.surveyperson + '\\' \
                    + i.filetype+ repr(i.idsurveyattribute) + '\\'+'检查报告'+'\\'
        # 总的点位数据和分析报告存放路径
        file_path3 = os.path.abspath('.') + "\\files_download\\" + i.pjid + '\\'
        all_name = os.path.abspath('.') + "\\files_download\\" + i.pjid + '\\' + i.pjid
        if not os.path.exists(file_path1):  # 判断文件夹是否存在
            os.makedirs(file_path1)  # 创建文件夹
        if not os.path.exists(file_path2):  # 判断文件夹是否存在
            os.makedirs(file_path2)  # 创建文件夹
        if not os.path.exists(file_path3):  # 判断文件夹是否存在
            os.makedirs(file_path3)  # 创建文件夹

        # 生成分析报告
        if not os.path.isfile(file_path2 + '分析报告.txt'):#判断文件是否存在
            obj_file = Surveyfile.objects.filter(Q(said__idsurveyattribute=i.idsurveyattribute),
                                                Q(filepath__contains='.cpf') |
                                                Q(filepath__contains='.svy') |
                                                Q(filepath__contains='.dc'))
            for j in obj_file:
                # 将文件路径简化
                j.filepath = j.filepath.split('\\')[7:]
                str = ' / '
                j.filepath = str.join(j.filepath)
                # 完成状态映射
                if j.said.isanalysed == 1:
                    j.said.isanalysed = '已分析'
                elif j.said.isanalysed == 0:
                    j.said.isanalysed = '未分析'
                else:
                    j.said.isanalysed = '文件不全'
                # 将检查数据写成文件
                all_check = CheckInformation.objects.filter(source__idsurveyattribute=i.idsurveyattribute). \
                    order_by("-log_level")
                for n in all_check:
                    if n.log_level=='error':
                        n.log_level='错误'
                    elif n.log_level=='warn':
                        n.log_level='警告'
                    else:
                        n.log_level='信息'
                with open(file_path2 + '分析报告.txt', 'w') as f:
                    for m in all_check:
                        f.write(m.source.pjid + ' ' + m.source.pjname + '  数据类型：' + m.source.filetype + '  状态：'+ j.said.isanalysed+ '\n')
                        f.write(j.filepath + '\n')
                        for n in all_check:
                            f.write(n.log_level + ' : ' + n.check_category  + '   ' + n.information+ '   ' + n.detail + '   ' + '\n')
                        f.write('\n')
                        break
                with open(all_name + '总分析报告.txt', 'a') as f:
                    for m in all_check:
                        f.write(m.source.pjid + ' ' + m.source.pjname + '  数据类型：' + m.source.filetype + '  状态：'+ j.said.isanalysed+ '\n')
                        f.write(j.filepath + '\n')
                        for n in all_check:
                            f.write(n.log_level + ' : ' + n.check_category  + '   ' + n.information+ '   ' + n.detail + '   ' + '\n')
                        f.write('\n')
                        break

        # 生成点位数据文件
        if not os.path.isfile(file_path2 + '点位数据.txt'):  # 判断文件是否存在
            file_points = Points2018.objects.filter(source__idsurveyattribute=i.idsurveyattribute)
            with open(file_path2 + '点位数据.txt', 'w') as f:
                for j in file_points:
                    f.write( repr(j.wkbgeometry.x)+',' +repr(j.wkbgeometry.y)+',' +repr(j.wkbgeometry.z)+','
                             +i.surveyperson+','+repr(i.surveytime))
                    f.write('\n')
            with open(all_name + '总点位数据.txt', 'w') as f:
                for j in file_points:
                    f.write( repr(j.wkbgeometry.x)+',' +repr(j.wkbgeometry.y)+',' +repr(j.wkbgeometry.z)+','
                             +i.surveyperson+','+repr(i.surveytime))
                    f.write('\n')

        # 生成外业文件
        all_files = Surveyfile.objects.filter(said__idsurveyattribute=i.idsurveyattribute)
        # 将外业文件写出来
        for j in all_files:
            path = os.path.split(j.filepath)
            file_name = path[1]  # 文件名
            if not os.path.isfile(file_path1 + file_name):  # 判断文件是否存在
                with open(file_path1 + file_name, 'wb') as f:
                    f.write(bytes(j.content))

    # 判断type值
    zip_path=''
    for i in test:
        # 外业文件夹路径
        file_path1 = os.path.abspath('.') + "\\files_download\\" + i.pjid + '\\' + i.surveyperson + '\\' \
                     + i.filetype + repr(i.idsurveyattribute) + '\\' + '外业文件' + '\\'
        # 检查报告文件夹路径
        file_path2 = os.path.abspath('.') + "\\files_download\\" + i.pjid + '\\' + i.surveyperson + '\\' \
                     + i.filetype + repr(i.idsurveyattribute) + '\\' + '检查报告' + '\\'
        # 总的点位数据和分析报告存放路径
        file_path3 = os.path.abspath('.') + "\\files_download\\" + i.pjid + '\\'
        # 所有点位数据和分析报告压缩后工程文件名
        zip_name = os.path.abspath('.') + "\\files_download\\ZIP\\" + i.pjid +'\\'+ i.pjid + '.zip'
        # 各个工程压缩文件存放路径
        zip_path=os.path.abspath('.') + "\\files_download\\ZIP\\" + i.pjid + '\\' + i.surveyperson + '\\' \
                     + i.filetype + repr(i.idsurveyattribute) + '\\'
        if not os.path.exists(zip_path):  # 判断文件夹是否存在
            os.makedirs(zip_path)  # 创建文件夹
    if flag=='1':
        file_name = "分析报告.txt"
        new_file_path = os.path.join(file_path2, file_name)
    elif flag=='2':
        file_name = "点位数据.txt"
        new_file_path = os.path.join(file_path2, file_name)
    elif flag=='3':
        name = os.path.join(zip_path, '外业原始文件.zip')#压缩后文件的绝对路径
        zip_ya(file_path1, name)
        new_file_path = os.path.join(zip_path, '外业原始文件.zip')#下载文件的绝对路径
    else:
        zip_ya(file_path3, zip_name)
        new_file_path = zip_name

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
        # 默认文件名不含中文
        # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        # 默认文件名含中文
        response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(new_file_path))

    except:
        return HttpResponse("Sorry but Not Found the File")
    return response


class ChangeSurveyperson(View):
    '''大组长和管理员可以修改测量员'''
    def get(self,request,idsurveyattribute,new_person):
        pass
        return render(request,'new_person.html',{

        })