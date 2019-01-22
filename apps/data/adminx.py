__author__ = 'zhu'
__date__ = '2019/1/17 10:22'

import xadmin
from .models import Surveyfile,Surveyattribute,CheckInformation,EfficiencyStatistic,Points2018


class SurveyfileAdmin(object):
    list_display = ['idsurveyfile','filepath','ctime','mtime','said','content']
    search_fields = ['idsurveyfile','ctime','mtime','said']
    list_filter = ['idsurveyfile','ctime','mtime','said']
    # 排序
    ordering=['-mtime']
    # 某些字段只读
    readonly_fields =['idsurveyfile','filepath','ctime','mtime','said','content']


class SurveyattributeAdmin(object):
    list_display = ['idsurveyattribute','pjid','pjname','surveyperson','surveytime','filetype','isanalysed']
    search_fields = ['idsurveyattribute','pjid','pjname','surveyperson','surveytime','filetype','isanalysed']
    list_filter = ['idsurveyattribute','pjid','pjname','surveyperson','surveytime','filetype','isanalysed']
    # 某些字段只读
    readonly_fields =['idsurveyattribute','pjid','pjname','surveyperson','surveytime','filetype','isanalysed']


class CheckInformationAdmin(object):
    list_display = ['check_category','log_level','information','detail','source','information_id']
    search_fields =['check_category','log_level','source','information_id']
    list_filter = ['check_category','log_level','source','information_id']
    # 某些字段只读
    readonly_fields =['check_category','log_level','information','detail','source','information_id']


class EfficiencyStatisticAdmin(object):
    list_display = ['statistic_id', 'source', 'start_time', 'end_time', 'number_point', 'survey_time', 'total_time']
    search_fields = ['statistic_id', 'source']
    list_filter = ['statistic_id', 'source']
    # 某些字段只读
    readonly_fields = ['statistic_id', 'source', 'start_time', 'end_time', 'number_point', 'survey_time', 'total_time']


class Points2018Admin(object):
    list_display = [ 'source', 'wkbgeometry', 'code', 'observe_time', 'geometry_id']
    search_fields = [ 'source',  'code', 'observe_time', 'geometry_id']
    list_filter = [ 'source', 'code', 'observe_time', 'geometry_id']
    # 某些字段只读
    readonly_fields = [ 'source', 'wkbgeometry', 'code', 'observe_time', 'geometry_id']







xadmin.site.register(Surveyfile, SurveyfileAdmin)
xadmin.site.register(Surveyattribute, SurveyattributeAdmin)
xadmin.site.register(CheckInformation, CheckInformationAdmin)
xadmin.site.register(EfficiencyStatistic, EfficiencyStatisticAdmin)
xadmin.site.register(Points2018, Points2018Admin)