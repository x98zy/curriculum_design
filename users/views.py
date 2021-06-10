from django.shortcuts import render,redirect,reverse
from django.http.response import HttpResponse
from django.views import View
from django.db.models import Q
from django.contrib.auth import authenticate,login,get_user_model,logout
from django.core.mail import send_mail
from finally_project.settings import EMAIL_FROM
from django.contrib.auth.hashers import make_password
from utils.get_news import get_news
from utils.read_news import read_news
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

from .forms import LoginForm,RegisterForm,LeavingMessageForm,MamageAccountForm,ManageInfoForm
from .models import LeavingMessage,EmailVerifyCode
from .forms import ChangePasswordForm,ResetPassWordForm,ConcatUsForm

import threading
import time,pytz
import os
from random import choice
from datetime import timedelta,datetime

User=get_user_model()


def generate_code(length=5):
    seed="AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    res=[]
    for i in range(length):
        res.append(choice(seed))
    return "".join(res)

def send_code(to,code):
    send_mail(subject="找回密码",message="您的验证码是{0},有效时间时间是2分钟".format(code),from_email=EMAIL_FROM,recipient_list=[to,])

class LoginView(View):
    def get(self,request):
        return render(request,"login1.html")
    def post(self,request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            username=request.POST.get("username","")
            password=request.POST.get("password","")
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('/index/')
            else:
                return render(request,"login1.html",{"msg":"用户名或密码错误"})
        else:
            return render(request,"login1.html",{"login_form":login_form})


class RegisterView(View):
    def post(self,request):
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            username=request.POST.get("username","")
            email=request.POST.get("email","")
            password1=request.POST.get("password1","")
            password2=request.POST.get("password2","")
            if User.objects.filter(email=email).count():
                return HttpResponse("该邮箱已被注册")
            if User.objects.filter(username=username).count():
                return HttpResponse("该用户已经存在")
            if password1!=password2:
                return HttpResponse("两次密码输入不一致")
            user=User(username=username)
            user.set_password(raw_password=password1)
            user.email=email
            user.save()
            login(request,user)
            return redirect('/index/')
        else:
            return HttpResponse("表单填写错误")


class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("users:login")



class IndexView(View):
    def get(self,request):
        #开启一个线程爬取网页数据，以防加载过慢
        thread1=threading.Thread(target=get_news,args=("http://www.agricoop.net/",))
        thread1.start()
        res=read_news()
        return render(request,"index1.html",{"res":res})


class AddLeavingMessageView(View):
    def post(self,request):
        leavingmessageform=LeavingMessageForm(request.POST)
        if leavingmessageform.is_valid():
            data=leavingmessageform.cleaned_data
            leavingmessage_instance=LeavingMessage(**data)
            leavingmessage_instance.save()
            return HttpResponse('{"status":"success","msg":"留言成功"}',content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"表单填写错误"}',content_type="application/json")


class Mamage_Account_View(View):
    @method_decorator(login_required(login_url="/users/login"))
    def get(self,request):
        return render(request,"manage_account.html")
    def post(self,request):
        manageaccountform=MamageAccountForm(request.POST,request.FILES)
        if manageaccountform.is_valid():
            username=manageaccountform.cleaned_data["username"]
            telephone=manageaccountform.cleaned_data["telephone"]
            email=manageaccountform.cleaned_data["email"]
            nick_name=manageaccountform.cleaned_data["nick_name"]
            user = self.request.user
            username_flag=False
            if User.objects.filter(username=username).count():
                return HttpResponse("该用户已被注册")
            if username and not username_flag:
                user.username=username
            if telephone and not User.objects.filter(telephone=telephone).count():
                user.telephone = telephone
            elif telephone:
                return HttpResponse("该手机已被注册")
            if email and not User.objects.filter(email=email).count():
                user.email = email
            elif email:
                return HttpResponse("该邮箱已被注册")
            if nick_name and not User.objects.filter(nick_name=nick_name).count():
                user.nick_name = nick_name
            elif nick_name:
                return HttpResponse("该昵称已被注册")
            if request.FILES:
                img = manageaccountform.cleaned_data["image"]
                add_time = time.strftime("%Y%m%d%H%M%S")
                ext = os.path.splitext(img.name)[1]
                img.name = add_time + ext
                file_path = os.path.join("media/images/users/", img.name)
                f = open(file_path, "wb")
                for line in img.chunks():
                    f.write(line)
                f.close()
                user.image = os.path.join("images/users/", img.name)
            user.save()
            return render(request, "manage_account.html")
        else:
            return HttpResponse("表单填写错误")


class ManageInfoView(View):
    @method_decorator(login_required(login_url="/users/login"))
    def get(self,request):
        return render(request,"manage_account.html")
    def post(self,request):
        mangageinfoform=ManageInfoForm(request.POST)
        if mangageinfoform.is_valid():
            school=mangageinfoform.cleaned_data["school"]
            major=mangageinfoform.cleaned_data["major"]
            company=mangageinfoform.cleaned_data["company"]
            my_desc=mangageinfoform.cleaned_data["my_desc"]
            user=self.request.user
            if school:
                user.school=school
            if major:
                user.major=major
            if company:
                user.company=company
            if my_desc:
                user.my_desc=my_desc
            user.save()
            return render(request,"manage_account.html")
        else:
            return HttpResponse("表单填写错误")

class ChangePasswordView(View):
    @method_decorator(login_required(login_url="/users/login"))
    def get(self,request):
        return render(request,"manage_account.html")
    def post(self,request):
        changepasswordform=ChangePasswordForm(request.POST)
        if changepasswordform.is_valid():
            original_password=changepasswordform.cleaned_data["original_password"]
            user=self.request.user
            if not user.check_password(original_password):
                return HttpResponse("原始密码输入错误")
            password1=changepasswordform.cleaned_data["password1"]
            password2=changepasswordform.cleaned_data["password2"]
            if password1!=password2:
                return HttpResponse("两次密码输入不一致")
            user.set_password(password1)
            user.save()
            login(request,user)
            return render(request,"manage_account.html")
        else:
            return HttpResponse("表单填写错误")


class ResetPasswordView(View):
    def get(self,request):
        return render(request,"reset_password.html")

    def post(self,request):
        email=request.POST.get("email","")
        user = User.objects.filter(email=email)
        if not email:
            return render(request,'reset_password.html',{"msg":'邮箱是必填的'})
        if not user:
            return render(request,'reset_password.html',{"msg":'该邮箱未被注册'})
        code=generate_code()
        email_code_instance=EmailVerifyCode(code=code,user=user[0],email=email)
        email_code_instance.save()
        send_code(to=email,code=code)
        return render(request,'set_password.html')

class SetPasswordView(View):
    def get(self,request):
        return render(request,"set_password.html")

    def post(self,request):
        setpasswordform=ResetPassWordForm(request.POST)
        if setpasswordform.is_valid():
            code=setpasswordform.cleaned_data["code"]
            password1=setpasswordform.cleaned_data["password1"]
            password2=setpasswordform.cleaned_data["password2"]
            two_minutes_age=datetime.now()-timedelta(hours=0,minutes=2,seconds=0)
            code_records=EmailVerifyCode.objects.filter(code=code).order_by("-add_time")
            last_record=code_records[0]
            if not code:
                return render(request,"set_password.html",{"msg":"验证码是必填的"})
            if last_record:
                if last_record.add_time<two_minutes_age:
                    return render(request,"set_password.html",{"msg":"验证码过期"})
            else:
                return render(request,"set_password.html",{"msg":"验证码错误"})
            if not password1 or not password2:
                return render(request,"set_password.html",{"msg":"密码是必填的"})
            if password1!=password2:
                return render(request,"set_password.html",{"msg":"两次密码输入不一致"})
            email=EmailVerifyCode.objects.get(code=code).email
            user=User.objects.get(email=email)
            user.set_password(password1)
            user.save()
            return redirect('/users/login')
        else:
            return render(request,"set_password.html",{"msg":"表单填写错误"})


class ConcatUsView(View):
    def get(self,request):
        return render(request,'concact_us.html')



class ConcatView(View):
    #接收ajax请求
    def post(self,request):
        concatform=ConcatUsForm(request.POST)
        if concatform.is_valid():
            return HttpResponse('{"status":"success","msg":"留言成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"表单填写错误"}',content_type="application/json")



class ProductIntroductView(View):
    def get(self,request):
        return render(request,'product_introdiction.html')
