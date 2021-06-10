from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# Create your models here.


class UserProfile(AbstractUser):
    image=models.ImageField(upload_to="images/users/%Y/%m/%d",default="images/users/messi.jpg",verbose_name="头像")
    telephone=models.CharField(max_length=11,verbose_name="电话")
    address=models.CharField(max_length=100,verbose_name="地址")
    nick_name=models.CharField(max_length=50,verbose_name="昵称")
    my_desc=models.CharField(max_length=300,verbose_name="自我简介",null=True,blank=True)
    school=models.CharField(max_length=60,verbose_name="学校",null=True,blank=True)
    major=models.CharField(max_length=60,verbose_name="专业",null=True,blank=True)
    company=models.CharField(max_length=60,verbose_name="公司",null=True,blank=True)


    class Meta:
        verbose_name="用户"
        verbose_name_plural=verbose_name


class LeavingMessage(models.Model):
    name=models.CharField(max_length=50,verbose_name="姓名",null=False,blank=False)
    subject=models.CharField(max_length=50,verbose_name="主题",null=False,blank=False)
    email=models.CharField(max_length=50,verbose_name="邮箱",null=False,blank=False)
    phone=models.CharField(max_length=50,verbose_name="电话",null=False,blank=False)
    message=models.TextField(verbose_name="留言主体",null=False,blank=False)

    class Meta:
        verbose_name="留言"
        verbose_name_plural=verbose_name


class EmailVerifyCode(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="用户")
    email=models.CharField(max_length=60,verbose_name="验证邮箱")
    code=models.CharField(max_length=11,verbose_name="验证码")
    add_time=models.DateTimeField(auto_now_add=True,verbose_name="添加时间")

    class Meta:
         verbose_name="验证码"
         verbose_name_plural=verbose_name