from django.urls import path

from .views import DeviceAddView,DeviceListView,DeviceInfoDetailView,DeleteDeviceView,VideoPlayView
urlpatterns=[
    path("add",DeviceAddView.as_view(),name="add"),
    path("list",DeviceListView.as_view(),name="list"),
    path("detail/<device_id>",DeviceInfoDetailView.as_view(),name="detail"),
    path("delete/<device_id>",DeleteDeviceView.as_view(),name="delete"),
    path("videoplay",VideoPlayView.as_view(),name="videoplay"),
]
