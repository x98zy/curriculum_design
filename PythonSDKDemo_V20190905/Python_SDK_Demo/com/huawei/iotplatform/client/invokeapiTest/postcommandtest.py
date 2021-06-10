import sys

sys.path.insert(0,'C:/Users/admin/Desktop/PythonSDK_V20190905/Python_SDK_Demo')
sys.path.insert(0,"E:/envs/IOT_LIGHT/Lib/site-packages/PythonSDK_V20190905")


from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.Authentication import Authentication
from Python_SDK_Demo.com.huawei.iotplatform.constant.Constant import Constant
from Python_SDK_Demo.com.huawei.iotplatform.client.dto.PostDeviceCommandInDTO import PostDeviceCommandInDTO
from Python_SDK_Demo.com.huawei.iotplatform.client.dto.CommandDTOV4 import CommandDTOV4
from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.SignalDelivery import SignalDelivery

def classtodict(obj):
    dict={}
    for key in dir(obj):
        value=getattr(obj,key)
        if not key.startswith("__") and not callable(value):
            dict[key]=value
    return dict

if __name__=="__main__":
    authentication = Authentication()
    ag = authentication.getAuthToken(Constant().clientInfo())
    accesstoken = ag.split(",")[0].split(":")[1]

    #设置命令body格式
    commanddtov4 = CommandDTOV4()
    commanddtov4.serviceId = "streetlight"
    commanddtov4.method = "SWITCH_LIGHT"
    commanddtov4.paras = {"SWITCH_LIGHT":"OFF"}
    commanddtov4=classtodict(commanddtov4)


    #设置命令类
    postdevicecommandindto=PostDeviceCommandInDTO()
    postdevicecommandindto.setDeviceId("8e1a7c4a-31ee-4621-bf2e-f5a6a81c1b18")
    postdevicecommandindto.command=commanddtov4


    signaldelivery=SignalDelivery()
    print(type(postdevicecommandindto))
    print(signaldelivery.postDeviceCommand(postdevicecommandindto,appId=None,accessToken=accesstoken[1:-1]))




