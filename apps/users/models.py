from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    birthday=models.DateField(verbose_name=u'生日',null=True,blank=True)
    gender=models.CharField(verbose_name=u'性别',max_length=10,choices=(("male",u"男"),("fenale","女")),default=u"")
    user_type = models.CharField(verbose_name="用户类型",max_length=50, choices=(("s_group_leader", "小组长"), ("b_group_leader", "大组长"),
                                                         ("administrator", "管理员")), default="小组长")
    mobile=models.CharField(verbose_name="联系电话",max_length=11,null=True,blank=True)
    image=models.ImageField(verbose_name='头像',upload_to="image/%Y/%m",default=u"image/avatar3.png",max_length=100)

    class Meta:
        verbose_name="用户信息"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.username
