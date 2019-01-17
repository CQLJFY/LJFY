__author__ = 'zhu'
__date__ = '2018/10/20 10:09'


import xadmin
from xadmin import views


# xadmin全局配置
class Basesetting(object):
    enable_themes=True
    use_bootswatch = True

class GlobalSetting(object):
    site_title = "重庆市勘测院后台管理系统"
    site_footer = "重庆市勘测院两江分院"
    # 下拉菜单
    menu_style='accordion'


xadmin.site.register(views.BaseAdminView,Basesetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)