import sys

sys.path.insert(0,'C:/Users/admin/Desktop/PythonSDK_V20190905/Python_SDK_Demo')
from Python_SDK_Demo.com.huawei.iotplatform.client.dto.CommandDTOV4 import CommandDTOV4


class PostDeviceCommandInDTO(object):
    command = CommandDTOV4()

    def __init__(self):
        self.deviceId = None
        self.callbackUrl = None
        self.expireTime = None
        self.maxRetransmit = None

    def getDeviceId(self):
        return self.deviceId

    def setDeviceId(self, deviceId):
        self.deviceId = deviceId

    def getCallbackUrl(self):
        return self.callbackUrl

    def setCallbackUrl(self, callbackUrl):
        self.callbackUrl = callbackUrl

    def getExpireTime(self):
        return self.expireTime

    def setExpireTime(self, expireTime):
        self.expireTime = expireTime

    def getMaxRetransmit(self):
        return self.maxRetransmit

    def setMaxRetransmit(self, maxRetransmit):
        self.maxRetransmit = maxRetransmit

    def getCommand(self):
        return self.command

    def setCommand(self, command):
        self.command = command
