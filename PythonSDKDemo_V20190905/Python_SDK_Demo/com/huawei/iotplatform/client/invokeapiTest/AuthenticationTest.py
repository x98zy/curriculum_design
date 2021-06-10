import json
import sys

sys.path.insert(0,'E:/djangoprojects/finally_project/PythonSDKDemo_V20190905')
sys.path.insert(0,"E:/envs/finall_project/Lib/site-packages/PythonSDK_V20190905")

from PythonSDK_V20190905.com.huawei.iotplatform.client.invokeapi.Authentication import Authentication

from Python_SDK_Demo.com.huawei.iotplatform.client.dto.AuthOutDTO import AuthOutDTO
from Python_SDK_Demo.com.huawei.iotplatform.client.dto.AuthRefreshInDTO import AuthRefreshInDTO
from Python_SDK_Demo.com.huawei.iotplatform.constant.Constant import Constant


class AuthenticationTest(object):

    def refreshAuthTokenInfo(self):
        arInDTO = AuthRefreshInDTO()
        arInDTO.appId = (Constant().readConfFile())[2]
        arInDTO.secret = (Constant().readConfFile())[3]
        authOutDTO = AuthOutDTO()
        result = Authentication().getAuthToken(Constant().clientInfo())
        authOutDTO.setRefreshToken(json.loads(result)['refreshToken'])
        arInDTO.refreshToken = authOutDTO.getRefreshToken()
        return arInDTO


if __name__ == "__main__":
    auTest = AuthenticationTest()
    authentication = Authentication()

    ag = authentication.getAuthToken(Constant().clientInfo())
    print("====== get access token ======")
    print("result:", ag + "\n")

    ar = authentication.refreshAuthToken(auTest.refreshAuthTokenInfo())
    print("====== refresh token ======")
    print("result:", ar + "\n")
