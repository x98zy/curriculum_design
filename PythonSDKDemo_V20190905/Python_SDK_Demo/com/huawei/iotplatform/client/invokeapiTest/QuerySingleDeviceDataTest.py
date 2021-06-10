"""查询单个设备信息"""

import sys
import json

sys.path.insert(0,'C:/Users/admin/Desktop/PythonSDK_V20190905/Python_SDK_Demo')
sys.path.insert(0,"E:/envs/IOT_LIGHT/Lib/site-packages/PythonSDK_V20190905")

from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.Authentication import Authentication
from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.DataCollection import DataCollection
from Python_SDK_Demo.com.huawei.iotplatform.constant.Constant import Constant



if __name__=="__main__":
    authentication = Authentication()
    ag = authentication.getAuthToken(Constant().clientInfo())
    accesstoken = ag.split(",")[0].split(":")[1]

    datacollection=DataCollection()

    collect_data=datacollection.querySingleDeviceInfo(deviceId="a3a3d33e-4f6a-40d0-a104-7e4254273112",appId=None,select="imsi",accessToken=accesstoken[1:-1])
    print(collect_data)



