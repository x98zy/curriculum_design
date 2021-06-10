# coding=GBK
from django import  forms
from django.contrib.auth import get_user_model

from .models import LeavingMessage
from django.forms import fields

User=get_user_model()

class LoginForm(forms.Form):
    username=forms.CharField(max_length=20,required=True)
    password=forms.CharField(max_length=30,required=True)

class RegisterForm(forms.Form):
    username=forms.CharField(max_length=20,required=True)
    email=forms.EmailField(max_length=50,required=True)
    password1=forms.CharField(max_length=20,required=True)
    password2=forms.CharField(max_length=20,required=True)


class LeavingMessageForm(forms.ModelForm):
    class Meta:
        model=LeavingMessage
        fields="__all__"


class MamageAccountForm(forms.Form):
    username=forms.CharField(max_length=50,required=False)
    telephone=forms.CharField(max_length=11,min_length=11,required=False)
    email=forms.EmailField(max_length=60,required=False)
    nick_name=forms.CharField(max_length=50,required=False)
    image=forms.FileField(required=False)


class ManageInfoForm(forms.Form):
    my_desc=forms.CharField(max_length=50,required=False)
    school=forms.CharField(max_length=50,required=False)
    major=forms.CharField(max_length=50,required=False)
    company=forms.CharField(max_length=50,required=False)

class ChangePasswordForm(forms.Form):
    original_password=forms.CharField(max_length=60,required=True)
    password1=forms.CharField(max_length=60,required=True)
    password2=forms.CharField(max_length=60,required=True)

class ResetPassWordForm(forms.Form):
    code = forms.CharField(max_length=10,required=True,error_messages={"required": "邮箱是必填的"})
    password1 = forms.CharField(max_length=60, required=True,error_messages={"required": "密码是必填的"})
    password2 = forms.CharField(max_length=60, required=True,error_messages={"required": "密码是必填的"})


class ConcatUsForm(forms.Form):
    name=forms.CharField(required=True)
    email=forms.EmailField(required=True)
    service=forms.CharField(required=True)
    message=forms.CharField(required=True)


