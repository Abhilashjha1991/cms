from django.urls import path, include ,re_path
from . import views

app_name="mainapp"

urlpatterns = [
    re_path('login/',views.login_user,name="loginuser"),
    re_path('user_detail/',views.user_detail,name="user_detail"),
    re_path('site_by_user/',views.site_by_user,name="site_by_user"),
    re_path('device_from_siteid/',views.device_from_siteid,name="device_from_siteid"),
    re_path('get_upload_video/', views.get_upload_video, name='get_upload_video'),

    # re_path('device_by_ev/',views.device_by_ev,name="device_by_ev"),
    # re_path('node_by_ev/',views.node_by_ev,name="node_by_ev"),
    # re_path('node_by_device/',views.node_by_device,name="node_by_device"),
    re_path('create_otp/',views.create_otp,name="create_otp"),
    re_path('Otp_verification/',views.Otp_verification,name="Otp_verification"),
    # re_path('forget_password/',views.forget_password),
    # re_path('update_password/',views.update_password),
    # path('alarm_history/',views.alarm_history),
]
