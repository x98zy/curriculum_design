from django.urls import path

from .views import LoginView,RegisterView,LogoutView,AddLeavingMessageView,Mamage_Account_View
from .views import ManageInfoView,ChangePasswordView,ResetPasswordView,SetPasswordView,ConcatUsView,ConcatView

urlpatterns=[
    path("login",LoginView.as_view(),name="login"),
    path('register',RegisterView.as_view(),name="register"),
    path("logout",LogoutView.as_view(),name="logout"),
    path("addmessage/",AddLeavingMessageView.as_view(),name="add_message"),
    path("manage_account",Mamage_Account_View.as_view(),name="manage_account"),
    path("manage_info",ManageInfoView.as_view(),name="manage_info"),
    path("change_password",ChangePasswordView.as_view(),name="change_password"),
    path('reset_password',ResetPasswordView.as_view(),name="reset_password"),
    path('set_password',SetPasswordView.as_view(),name="set_password"),
    path('concat_us',ConcatUsView.as_view(),name="concat_us"),
    path('concat/',ConcatView.as_view(),name="concat"),
]
