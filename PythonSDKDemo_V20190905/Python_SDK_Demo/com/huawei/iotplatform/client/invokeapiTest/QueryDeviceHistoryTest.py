"""查询设备历史数据"""

import sys

sys.path.insert(0,'C:/Users/admin/Desktop/PythonSDK_V20190905/Python_SDK_Demo')
sys.path.insert(0,"E:/envs/IOT_LIGHT/Lib/site-packages/PythonSDK_V20190905")

from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.Authentication import Authentication
from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.DataCollection import DataCollection
from Python_SDK_Demo.com.huawei.iotplatform.constant.Constant import Constant
from Python_SDK_Demo.com.huawei.iotplatform.client.dto.QueryDeviceDataHistoryInDTO import QueryDeviceDataHistoryInDTO


if __name__=="__main__":
    authentication = Authentication()
    ag = authentication.getAuthToken(Constant().clientInfo())
    accesstoken = ag.split(",")[0].split(":")[1]

    data_collection = DataCollection()
    devicedatahistorydto=QueryDeviceDataHistoryInDTO()


    devicedatahistorydto.setAppId(None)
    devicedatahistorydto.setDeviceId("8e1a7c4a-31ee-4621-bf2e-f5a6a81c1b18")
    devicedatahistorydto.setGatewayId("8e1a7c4a-31ee-4621-bf2e-f5a6a81c1b18")
    devicedatahistorydto.setPageSize(5)


    print(data_collection.queryDeviceDataHistory(qddhInDTO=devicedatahistorydto,accessToken=accesstoken[1:-1]))