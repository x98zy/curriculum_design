"""在设备接入物联网平台前，第三方应用需要调用此接口在物联网平台注册设备，并把设备的唯一标识码（
如IMEI）设置为设备接入平台的验证码。
在设备接入物联网平台时携带设备唯一标识，完成设备的接入认证"""
import sys
sys.path.insert(0,'E:/djangoprojects/finally_project/PythonSDKDemo_V20190905')
sys.path.insert(0,"E:/envs/finall_project/Lib/site-packages/PythonSDK_V20190905")
from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.DeviceManagement import DeviceManagement
from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.Authentication import Authentication
from Python_SDK_Demo.com.huawei.iotplatform.client.invokeapiTest.AuthenticationTest import AuthenticationTest
from Python_SDK_Demo.com.huawei.iotplatform.constant.Constant import Constant
from Python_SDK_Demo.com.huawei.iotplatform.client.dto.RegDirectDeviceInDTO import RegDirectDeviceInDTO
from Python_SDK_Demo.com.huawei.iotplatform.client.dto.DeviceInfoDTO import DeviceInfoDTO
if __name__=="__main__":
    autest=AuthenticationTest()
    authentication = Authentication()
    ag = authentication.getAuthToken(Constant().clientInfo())
    accesstoken=ag.split(",")[0].split(":")[1]
    deviceinfodto=DeviceInfoDTO()#表示要注册设备的信息，只需要填写设备model（型号）即可
    deviceinfodto.setModel("001A-0A12")#设置设备的型号
    deviceinfodto.setManufacturerId("8d2cb5b1888d459a914983c791e17bc1")
    deviceinfodto.manufacturerName="HUAWEI"
    deviceinfodto.setModel("streetlight001")
    deviceinfodto.setDeviceType("StreetLight")
    redirectdeviceindto=RegDirectDeviceInDTO()
    redirectdeviceindto.setNodeId("860411049886490")
    redirectdeviceindto.setDeviceName("device1")
    redirectdeviceindto.setProductId("5ffd922a22768f094ced7663")
    devicemanagement=DeviceManagement()
    #同一个NodeId只能注册一次，多次注册会导致设备异常
    print(devicemanagement.regDirectDevice(rddInDto=redirectdeviceindto,appId="phe7GWM_ySUT3H2fuQPaIoh8F68a",accessToken=accesstoken[1:-1]))