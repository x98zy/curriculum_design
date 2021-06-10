"""批量查询设备信息"""

import sys

sys.path.insert(0,'C:/Users/admin/Desktop/PythonSDK_V20190905/Python_SDK_Demo')
sys.path.insert(0,"E:/envs/IOT_LIGHT/Lib/site-packages/PythonSDK_V20190905")

from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.Authentication import Authentication
from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.DataCollection import DataCollection
from Python_SDK_Demo.com.huawei.iotplatform.constant.Constant import Constant
from Python_SDK_Demo.com.huawei.iotplatform.client.dto.QueryBatchDevicesInfoInDTO import QueryBatchDevicesInfoInDTO


if __name__=="__main__":
    authentication = Authentication()
    ag = authentication.getAuthToken(Constant().clientInfo())
    accesstoken = ag.split(",")[0].split(":")[1]

    data_collection=DataCollection()
    querybatchdevicesinfoindto=QueryBatchDevicesInfoInDTO()
    querybatchdevicesinfoindto.setAppId(None)
    #查询在线设备的数据
    querybatchdevicesinfoindto.setStatus("ONLINE")

    print(data_collection.queryBatchDevicesInfo(qbdiInDTO=querybatchdevicesinfoindto,accessToken=accesstoken[1:-1]))