import json
import sys


from django.shortcuts import render,redirect
from django.views import View

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import urllib.parse
# Create your views here.

from .forms import DeviceForm
from .models import Device,Video

from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.DeviceManagement import DeviceManagement
from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.Authentication import Authentication
from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.DataCollection import DataCollection
from Python_SDK_Demo.com.huawei.iotplatform.constant.Constant import Constant
from Python_SDK_Demo.com.huawei.iotplatform.client.dto.RegDirectDeviceInDTO import RegDirectDeviceInDTO
from Python_SDK_Demo.com.huawei.iotplatform.client.dto.DeviceInfoDTO import DeviceInfoDTO
from Python_SDK_Demo.com.huawei.iotplatform.client.dto.QueryBatchDevicesInfoInDTO import QueryBatchDevicesInfoInDTO
from Python_SDK_Demo.com.huawei.iotplatform.client.dto.QueryDeviceDataHistoryInDTO import QueryDeviceDataHistoryInDTO




sys.path.insert(0,'/data/env/pyweb/lib/python3.6/site-packages')
sys.path.insert(0,'/data/wwwroot/finally_project/PythonSDKDemo_V20190905/Python_SDK_Demo')


from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import time


from datetime import datetime,timedelta

logging.basicConfig(level=logging.INFO,stream=sys.stdout)

secret_id="AKIDToywiHcoslQr30iBQREqIWXJsCIAnDYo"
secret_key="TqBSiwyoTxFJ9l8JNSSFnxxlLhtwvrgR"
region="ap-nanjing"
token=None
scheme="https"
endpoint = 'cos.ap-nanjing.myqcloud.com'
config=CosConfig(Region=region,SecretId=secret_id,SecretKey=secret_key,Token=token,Scheme=scheme)
#设置云对象上传客户端
client=CosS3Client(config)

#将类中的属性转换为字典以便可以序列化
def clastodict(obj):
    dict={}
    for key in dir(obj):
        value=getattr(obj,key)
        if not key.startswith("__") and not callable(value):
            dict[key]=value
    return dict


def change_timestamp_to_realtime(timestamp):
    day_time=timestamp.split("T")[0]
    return_day=""+day_time[0:4]+":"+day_time[4:6]+":"+day_time[6:8]
    second_time=timestamp.split("T")[1]
    return_time=""+second_time[0:2]+":"+second_time[2:4]+":"+second_time[4:6]
    return return_day+":"+return_time


class DeviceAddView(View):
    @method_decorator(login_required(login_url="/users/login"))
    def get(self,request):
        return render(request, "add_device.html", {})
    def post(self,request):
        device_name=request.POST.get("device_name","")
        imsi=request.POST.get("imsi","")
        device_form=DeviceForm(request.POST)
        if device_form.is_valid():
            device_instance=Device()
            authentication = Authentication()
            ag = authentication.getAuthToken(Constant().clientInfo())
            accesstoken = ag.split(",")[0].split(":")[1]


            deviceinfodto = DeviceInfoDTO()  # 表示要注册设备的信息，只需要填写设备model（型号）即可
            deviceinfodto.setModel("00000001")  # 设置设备的型号
            deviceinfodto.setManufacturerId("8d2cb5b1888d459a914983c791e17bc1")#设置厂商ID
            deviceinfodto.setmanufacturerName("HUAWEI")#设置厂商名
            deviceinfodto.setDeviceType("MultiSensor")#设置设备类型
            deviceinfodto.setProtocolType("LWM2M")#设置设备协议
            deviceinfodto=clastodict(deviceinfodto)

            redirectdeviceindto = RegDirectDeviceInDTO()
            redirectdeviceindto.deviceInfo=deviceinfodto
            redirectdeviceindto.setDeviceName(device_name)
            redirectdeviceindto.setNodeId(imsi)
            redirectdeviceindto.setProductId("604219a122768f094ccb74b1")

            device_management=DeviceManagement()
            return_data=device_management.regDirectDevice(rddInDto=redirectdeviceindto,appId="Y2fIeoKaw4Sizm0lZjGOZNfhRkoa",accessToken=accesstoken[1:-1])

            return_date_dict=json.loads(return_data)
            device_instance.device_id=return_date_dict["deviceId"]
            device_instance.user=request.user
            device_instance.device_name=device_name
            device_instance.belonged_product="jujube_environment"
            device_instance.product_type="MultiSensor"
            device_instance.save()

            return redirect(to="/device/list")


class DeviceListView(View):
    @method_decorator(login_required(login_url="/users/login"))
    def get(self,request):
        authentication = Authentication()
        ag = authentication.getAuthToken(Constant().clientInfo())
        accesstoken = ag.split(",")[0].split(":")[1]
        #获取设备列表前先更新设备状态
        data_collect=DataCollection()
        querybatchdevicesinfoindto=QueryBatchDevicesInfoInDTO()
        querybatchdevicesinfoindto.setPageSize('20')
        data=data_collect.queryBatchDevicesInfo(qbdiInDTO=querybatchdevicesinfoindto,accessToken=accesstoken[1:-1])
        devices=[]
        if json.loads(data).get("devices",""):
            devices=json.loads(data)["devices"]
        for device in devices:
            try:
                device_id = device["deviceId"]
                device_instance = Device.objects.get(device_id=device_id)
                device_instance.status = device['deviceInfo']['status']
                device_instance.save()
            except Exception as e:
                pass
        user=self.request.user
        devices=Device.objects.filter(user=self.request.user)
        online_num=Device.objects.filter(status="ONLINE").count()
        offline_num=Device.objects.filter(status="OFFLINE").count()
        err_num=Device.objects.filter(status="ABNORMAL").count()
        #求出离线设备和在线设备的比例
        try:
            online_num_res = online_num / (online_num + offline_num + err_num)
            offline_num_res = offline_num / (online_num + offline_num + err_num)
            err_num_res = err_num / (online_num + offline_num + err_num)
        except ZeroDivisionError as e:
            online_num_res=0
            offline_num_res=0
            err_num_res=0
        return render(request,"device_list.html",{"devices":devices,"online":online_num,"offline":offline_num,"err":err_num,"device_num":online_num+offline_num+err_num})


#根据设备ID查找设备的具体信息
class DeviceInfoDetailView(View):
    @method_decorator(login_required(login_url="/users/login"))
    def get(self,request,device_id):
        authentication = Authentication()
        ag = authentication.getAuthToken(Constant().clientInfo())
        accesstoken = ag.split(",")[0].split(":")[1]

        data_collect=DataCollection()
        data=data_collect.querySingleDeviceInfo(deviceId=device_id,appId=None,select="imsi",accessToken=accesstoken[1:-1])

        dict_data=json.loads(data)
        #获网关id以便查询历史数据时填入
        gatewayid=dict_data.get("gatewayId",None)

        querydatahistory=QueryDeviceDataHistoryInDTO()
        querydatahistory.setAppId(None)
        querydatahistory.setDeviceId(deviceId=device_id)
        querydatahistory.setGatewayId(gatewayId=gatewayid)
        querydatahistory.setPageSize(2000)
        histoty_data=data_collect.queryDeviceDataHistory(qddhInDTO=querydatahistory,accessToken=accesstoken[1:-1])

        dict_history_data=json.loads(histoty_data)
        histoty_dto=dict_history_data['deviceDataHistoryDTOs']
        return_data=[]
        time_data=[]
        for dto in histoty_dto:
            if dto["data"]["mark"]==0:
                continue
            else:
                return_data.append(dto["data"])
                timestamp=datetime.strptime(dto["timestamp"],"%Y%m%dT%H%M%SZ")
                fd=(timestamp+timedelta(hours=8)).strftime("%Y-%m-%d:%H:%M:%S")
                time_data.append(fd)
                #time_data.append(change_timestamp_to_realtime(dto["timestamp"])[5:])
        for i in range(len(return_data)):
            return_data[i].__delitem__("mark")
        data=zip(return_data,time_data)
        AirTemp,AirHumidity,LightIntensity,OilHumidity = [],[],[],[]
        for single_dict in return_data:
            AirTemp.append(single_dict["AirTemp"])
            AirHumidity.append(single_dict["AirHumidity"])
            LightIntensity.append(single_dict["LightIntensity"]//100)
            OilHumidity.append(single_dict["SoilHumidity"]//100)
        return render(request,"detail.html",{"data":data,"AirTemp":AirTemp,"AirHumidity":AirHumidity,"LightIntensity":LightIntensity,"OilHumidity":OilHumidity,"time_data":time_data})

class DeleteDeviceView(View):
    @method_decorator(login_required(login_url="/users/login"))
    def post(self,request,device_id):
        device_instance=Device.objects.get(Q(device_id=device_id)& Q(user=request.user))
        device_instance.delete()
        authentication = Authentication()
        ag = authentication.getAuthToken(Constant().clientInfo())
        accesstoken = ag.split(",")[0].split(":")[1]

        device_management=DeviceManagement()
        device_management.deleteDirectDevice(deviceId=device_id,accessToken=accesstoken[1:-1],cascade="true",appId=None)
        return redirect(to="/device/list")

class VideoPlayView(View):
    def get(self,request):
        return render(request,'video_play.html')



class UploadView(View):
    @method_decorator(login_required(login_url="/users/login"))
    def get(self,request):
        return render(request,"uploadvideo.html")
    def post(self,request):
        #通过parse方法获取视频名称
        video_name=urllib.parse.unquote(request.headers.get("Name"))
        #body是传输过来的视频数据
        video=request.body
        client.put_object(
            Bucket='first-1257059002',
            Body=video,
            Key="video/{}".format(video_name),
            StorageClass='STANDARD',
            EnableMD5=False,
        )
        video_instane=Video()
        video_instane.user=request.user
        video_instane.name=video_name
        video_instane.path="https://first-1257059002.cos.ap-nanjing.myqcloud.com/video/"+request.headers.get("Name")
        video_instane.save()
        return HttpResponse("OK",status=200)


class DisplayVideoView(View):
    def get(self,request):
        videos=Video.objects.all()
        return render(request,"display_video.html",{"videos":videos})
