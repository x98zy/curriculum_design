from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User=get_user_model()

class Device(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="所属用户")
    status=models.CharField(max_length=20,choices=(("OFFLINE","离线"),("ONLINE","在线"),("ABNORMAL","异常")),verbose_name="设备状态",default="OFFLINE")
    device_name=models.CharField(max_length=50,verbose_name="设备名称")
    device_id=models.CharField(max_length=100,verbose_name="设备ID")
    belonged_product=models.CharField(max_length=30,verbose_name="所属产品")
    product_type=models.CharField(max_length=30,verbose_name="设备类型")

    class Meta:
        verbose_name="设备"
        verbose_name_plural=verbose_name


class Video(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="所属用户")
    path=models.CharField(max_length=500,verbose_name="视频存储路径")
    name=models.CharField(max_length=200,verbose_name="视频名称")
    add_time=models.DateTimeField(auto_now_add=True,verbose_name="添加时间")
    class Meta:
        verbose_name="视频对象"
        verbose_name_plural=verbose_name
