"""LJFY URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import xadmin
from django.urls import path,include
from django.views.static import serve

from users.views import LoginView,IndexView,LogoutView
from LJFY.settings import MEDIA_ROOT

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('',LoginView.as_view(),name="login"),
    path('index/',IndexView.as_view(),name='index'),
    path('logout/', LogoutView.as_view(), name="logout"),

    #项目数据url配置
    path('pj/', include(('data.urls','data'), namespace="pj")),


    # 配置上传文件的访问处理函数
    path('media/<path>/', serve, {"document_root":MEDIA_ROOT}),
]
