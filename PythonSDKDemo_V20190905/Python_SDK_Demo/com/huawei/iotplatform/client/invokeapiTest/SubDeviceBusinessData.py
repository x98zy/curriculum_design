"""订阅平台业务数据"""

import sys

sys.path.insert(0,'C:/Users/admin/Desktop/PythonSDK_V20190905/Python_SDK_Demo')
sys.path.insert(0,"E:/envs/IOT_LIGHT/Lib/site-packages/PythonSDK_V20190905")

from Python_SDK_Demo.com.huawei.iotplatform.client.dto.SubDeviceBusinessDataInDTO import SubDeviceBusinessDataInDTO
from Python_SDK_Demo.com.huawei.iotplatform.constant.Constant import Constant
from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.Authentication import Authentication
from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.SubscriptionManagement import SubscriptionManagement

if __name__=="__main__":
    authentication = Authentication()
    ag = authentication.getAuthToken(Constant().clientInfo())
    accesstoken = ag.split(",")[0].split(":")[1]

    subdevicedatadto=SubDeviceBusinessDataInDTO()
    #订阅设备数据发生变化时向服务器发送消息
    subdevicedatadto.setNotifyType("deviceDataChanged")
    subdevicedatadto.setOwnerFlag("true")
    subdevicedatadto.setCallbackUrl("http://121.36.37.188:443/reveiver/datachange")

    data_collect=SubscriptionManagement()
    print(data_collect.subDeviceBusinessData(subdevicedatadto,accesstoken[1:-1]))



