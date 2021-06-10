"""finally_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path,include
from .settings import MEDIA_URL,MEDIA_ROOT
from django.views.generic import TemplateView
from users.views import IndexView,ProductIntroductView
from device.views import UploadView,DisplayVideoView



urlpatterns = [
    path('admin/', admin.site.urls),
    path("displayvideo",DisplayVideoView.as_view(),name="displayvideo"),
    path("uploadvideo",UploadView.as_view(),name="uploadvideo"),
    path("users/",include(("users.urls","users"),namespace="users")),
    path("index/",IndexView.as_view(),name="index"),
    path("device/",include(("device.urls","device"),namespace="device")),
    path("product_introduction/",ProductIntroductView.as_view(),name="product_introduction"),
]
urlpatterns += static(MEDIA_URL,document_root=MEDIA_ROOT)
