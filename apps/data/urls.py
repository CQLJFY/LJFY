__author__ = 'zhu'
__date__ = '2018/10/24 14:43'

from django.urls import path,re_path
from .views import pj_data,files_download,ChangeSurveyperson

urlpatterns = [
    # 项目数据
    path('data/', pj_data.as_view(), name='pj_data'),
    # 下载文件
    re_path('download/(?P<idsurveyattribute>\d+)/(?P<flag>\d+)/',files_download,name='download'),
    # 修改测量员
    # path('person_save/(?P<idsurveyattribute>\d+)/(?P<new_person>\d+)/',ChangeSurveyperson.as_view(),name='person_save'),


]