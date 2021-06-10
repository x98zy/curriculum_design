from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class DeviceConfig(AppConfig):
    name = 'device'
    # def ready(self):
    #    autodiscover_modules('socket_server')
