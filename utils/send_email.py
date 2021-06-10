# coding=utf-8
from django.core.mail import send_mail
from finally_project.settings import EMAIL_FROM


from random import choice
import os,sys
pwd=os.path.dirname(os.path.dirname(os.path.realpath("__file__")))
#sys.path.append(pwd+"../")

os.environ.setdefault("DJANGO_SETTINGS_MODULE","finally_project.settings")

def generate_code(length=5):
    seed="AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    res=[]
    for i in range(length):
        res.append(choice(seed))
    return "".join(res)

def send_code(code=generate_code()):
    send_mail(subject="找回密码",message="您的验证码是{0},有效时间时间是2分钟".format(code),from_email=EMAIL_FROM,recipient_list=["1580987871@qq.com",])

if __name__=="__main__":
    send_code()