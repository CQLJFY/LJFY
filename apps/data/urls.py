__author__ = 'zhu'
__date__ = '2018/10/24 14:43'

from django.urls import path,re_path
from .views import pj_data,file_down

urlpatterns = [
    # 项目数据
    path('data/', pj_data.as_view(), name='pj_data'),
    # 下载分析报告
    re_path('download/(?P<id>\d+)',file_down,name='download'),


]