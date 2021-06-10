"""在物联网平台出删除设备"""

"""已在物联网平台注册的设备，若不再需要接入平台时，第三方应用可调用此接口在
物联网平台删除设备。后续若设备要再次接入平台，第三方应用需要在物联网平台重新注
册设备。"""

import sys

sys.path.insert(0,'C:/Users/admin/Desktop/PythonSDK_V20190905/Python_SDK_Demo')
sys.path.insert(0,"E:/envs/IOT_LIGHT/Lib/site-packages/PythonSDK_V20190905")

from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.DeviceManagement import DeviceManagement
from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.Authentication import Authentication
from Python_SDK_Demo.com.huawei.iotplatform.constant.Constant import Constant

if __name__=="__main__":
    authentication = Authentication()
    ag = authentication.getAuthToken(Constant().clientInfo())
    accesstoken = ag.split(",")[0].split(":")[1]

    devicemanagement=DeviceManagement()
    devicemanagement.deleteDirectDevice(deviceId="ae8bf573-5edd-4259-ac14-068ba6f98ea5",cascade=None,appId="phe7GWM_ySUT3H2fuQPaIoh8F68a",accessToken=accesstoken[1:-1])