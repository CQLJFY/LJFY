from django.shortcuts import render
import  json

from django.shortcuts import render
from django.contrib.auth import login,logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q


from .models import UserProfile
from .form import LoginForm
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.

class CustomBackend(ModelBackend):
    '''可以通过邮箱登录'''
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class LogoutView(View):
    """
    用户退出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))

class LoginView(View):
    # 用户登录
    def get(self, request):
        return render(request, "login.html", {})
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = CustomBackend.authenticate(self,username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg":"用户未激活！"})
            else:
                return render(request, "login.html", {"msg":"用户名或密码错误！"})
        else:
            return render(request, "login.html", {"login_form":login_form})


class IndexView(LoginRequiredMixin,View):
    #重庆市勘测院 首页
    def get(self, request):
        return render(request, 'index.html', {

        })